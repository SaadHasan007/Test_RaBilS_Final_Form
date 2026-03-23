import React from 'react';

// ─────────────────────────────────────────────────────────────────────────────
// TEST_CASE_SCHEMA
// This is the single source of truth for the test case table structure.
//
// Each entry defines:
//   label – the column header displayed in the table
//   field – the key used in every test case data object
//
// When your trained model is ready, make it return an array of objects where
// each object has exactly these field names, then pass that array as the
// `testCaseRows` prop directly to <TestCasesDisplay /> — no other changes needed.
//
// Example object your model should produce per test case:
// {
//   testCaseId:    "TC-001",
//   requirementId: "REQ-001",
//   testCase:      "User logs in with valid credentials",
//   precondition:  "User has a registered account",
//   steps:         ["Open login page", "Enter credentials", "Click Login"],
//   expectedResult:"User is redirected to the dashboard",
//   priority:      "High",
// }
// ─────────────────────────────────────────────────────────────────────────────
export const TEST_CASE_SCHEMA = [
  { label: 'Test Case ID',    field: 'testCaseId'    },
  { label: 'Requirement ID',  field: 'requirementId' },
  { label: 'Test Case',       field: 'testCase'      },
  { label: 'Precondition',    field: 'precondition'  },
  { label: 'Test Steps',      field: 'steps'         },  // value must be an array of strings
  { label: 'Expected Result', field: 'expectedResult'},
  { label: 'Priority',        field: 'priority'      },
];


// ─────────────────────────────────────────────────────────────────────────────
// parseGherkinToSchema
// Converts a raw Gherkin string → array of objects whose keys match TEST_CASE_SCHEMA.
// This is used NOW (before the trained model is attached).
// Once you plug-in the model you can REPLACE this function entirely; the table
// component below will keep working because it only reads the schema fields.
// ─────────────────────────────────────────────────────────────────────────────
function parseGherkinToSchema(gherkin) {
  if (!gherkin) return [];

  const lines = gherkin.split('\n');
  const intermediate = [];   // raw parsed scenarios
  let current = null;
  let inPrecondition = true;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (line.startsWith('Scenario:') || line.startsWith('Scenario Outline:')) {
      if (current) intermediate.push(current);
      current = {
        testCase: line.replace(/^Scenario(?: Outline)?:\s*/i, '').trim(),
        preconditionParts: [],
        stepParts: [],
        expectedResultParts: [],
      };
      inPrecondition = true;
      continue;
    }

    if (!current) continue;

    if (line.startsWith('Given ')) {
      current.preconditionParts.push(line.replace(/^Given\s+/i, '').trim());
      inPrecondition = true;
      continue;
    }

    if (line.startsWith('When ')) {
      inPrecondition = false;
      current.stepParts.push(line.replace(/^When\s+/i, '').trim());
      continue;
    }

    if (line.startsWith('Then ')) {
      inPrecondition = false;
      const text = line.replace(/^Then\s+/i, '').trim();
      current.expectedResultParts.push(text);
      current.stepParts.push(text);
      continue;
    }

    if (line.startsWith('And ') || line.startsWith('But ')) {
      const text = line.replace(/^(?:And|But)\s+/i, '').trim();
      if (inPrecondition) {
        current.preconditionParts.push(text);
      } else {
        if (current.expectedResultParts.length > 0) current.expectedResultParts.push(text);
        current.stepParts.push(text);
      }
    }
  }

  if (current) intermediate.push(current);

  // Map to the exact field names defined in TEST_CASE_SCHEMA
  return intermediate.map((sc, idx) => ({
    testCaseId:    `TC-${String(idx + 1).padStart(3, '0')}`,
    requirementId: `REQ-${String(idx + 1).padStart(3, '0')}`,
    testCase:      sc.testCase || `Test Case ${idx + 1}`,
    precondition:  sc.preconditionParts.join('; ') || '—',
    steps:         sc.stepParts.length > 0 ? sc.stepParts : ['(no steps found)'],
    expectedResult:sc.expectedResultParts.join('; ') || sc.stepParts[sc.stepParts.length - 1] || '—',
    // `priority` is injected per-row in the component below (comes from the backend)
  }));
}


// ─── Priority badge ───────────────────────────────────────────────────────────
const PriorityBadge = ({ priority }) => {
  const color =
    priority === 'High'   ? 'text-red-400'    :
    priority === 'Medium' ? 'text-yellow-400' :
                            'text-green-400';
  return <span className={`font-semibold ${color}`}>{priority}</span>;
};


// ─── Cell renderer ────────────────────────────────────────────────────────────
// Handles the special cases: `steps` (array → numbered list), `priority` (badge).
const CellValue = ({ field, value, priority }) => {
  if (field === 'steps') {
    const items = Array.isArray(value) ? value : [value];
    return (
      <ol className="list-none space-y-1">
        {items.map((step, i) => (
          <li key={i} className="flex gap-2">
            <span className="text-blue-400 font-semibold shrink-0">{i + 1}.</span>
            <span>{step}</span>
          </li>
        ))}
      </ol>
    );
  }

  if (field === 'priority') {
    return <PriorityBadge priority={priority} />;
  }

  return <span>{value ?? '—'}</span>;
};


// ─── Main Component ───────────────────────────────────────────────────────────
// Props:
//   gherkin      – raw Gherkin string from the backend (used until model is attached)
//   priority     – "High" | "Medium" | "Low" from the backend
//   testCaseRows – (optional) pre-structured array from your trained model.
//                  When provided, `gherkin` is ignored and this data is displayed
//                  directly. Each object must have the field names in TEST_CASE_SCHEMA.
const TestCasesDisplay = ({ gherkin, priority, testCaseRows }) => {
  // Prefer model-supplied rows; fall back to parsing the Gherkin string
  const rows = testCaseRows ?? parseGherkinToSchema(gherkin);

  if (!rows || rows.length === 0) {
    if (!gherkin) return null;
    // Nothing parsed – raw fallback
    return (
      <div className="mt-8">
        <h2 className="text-2xl font-bold text-white mb-6">Generated Test Cases</h2>
        <pre className="p-6 rounded-xl bg-slate-900 border border-slate-800 text-blue-100 font-mono text-sm overflow-x-auto">
          {gherkin}
        </pre>
      </div>
    );
  }

  return (
    <div className="mt-8">
      <h2 className="text-3xl font-bold text-white text-center mb-8 tracking-tight">
        Generated Test Cases
      </h2>

      <div
        className="rounded-2xl overflow-hidden shadow-2xl"
        style={{
          background: 'rgba(15, 23, 50, 0.85)',
          border: '1px solid rgba(99, 132, 255, 0.2)',
          backdropFilter: 'blur(12px)',
        }}
      >
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-sm">

            {/* ── Header – driven by TEST_CASE_SCHEMA labels ── */}
            <thead>
              <tr
                style={{
                  background: 'linear-gradient(90deg, #1e2a6e 0%, #1a237e 100%)',
                  borderBottom: '2px solid rgba(99, 132, 255, 0.3)',
                }}
              >
                {TEST_CASE_SCHEMA.map(({ label }) => (
                  <th
                    key={label}
                    className="px-4 py-4 text-left text-xs font-bold uppercase tracking-wider text-blue-200"
                    style={{ whiteSpace: 'nowrap' }}
                  >
                    {label}
                  </th>
                ))}
              </tr>
            </thead>

            {/* ── Body – driven by TEST_CASE_SCHEMA fields ── */}
            <tbody>
              {rows.map((row, rowIdx) => (
                <tr
                  key={row.testCaseId ?? rowIdx}
                  style={{
                    background: rowIdx % 2 === 0
                      ? 'rgba(20, 30, 70, 0.6)'
                      : 'rgba(12, 20, 55, 0.5)',
                    borderBottom: '1px solid rgba(99, 132, 255, 0.1)',
                  }}
                >
                  {TEST_CASE_SCHEMA.map(({ field }) => (
                    <td
                      key={field}
                      className="px-4 py-5 text-slate-200 align-top"
                      style={{ maxWidth: field === 'steps' ? 220 : 180 }}
                    >
                      <CellValue
                        field={field}
                        value={row[field]}
                        priority={row.priority ?? priority}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>

          </table>
        </div>
      </div>
    </div>
  );
};

export default TestCasesDisplay;
