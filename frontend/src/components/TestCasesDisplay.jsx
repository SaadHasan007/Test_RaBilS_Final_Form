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
