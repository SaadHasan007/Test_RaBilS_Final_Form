import React from 'react';

// ─── Gherkin Parser ───────────────────────────────────────────────────────────
/**
 * Parses a Gherkin feature string into an array of structured test-case objects.
 *
 * Each object has:
 *   id          – e.g. "TC-001"
 *   requirementId – e.g. "REQ-001"
 *   testCase    – scenario title
 *   precondition – text of the first Given block (joined)
 *   steps       – array of step strings (When / Then / And / But after Given)
 *   expectedResult – text collected after the last "Then" keyword
 */
function parseGherkin(gherkin) {
  if (!gherkin) return [];

  const lines = gherkin.split('\n');
  const scenarios = [];
  let current = null;
  // Track whether we've left the "Given" / precondition section
  let inPrecondition = true;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (line.startsWith('Scenario:') || line.startsWith('Scenario Outline:')) {
      // Save previous scenario
      if (current) scenarios.push(current);
      current = {
        testCase: line.replace(/^Scenario(?: Outline)?:\s*/i, '').trim(),
        preconditionParts: [],
        steps: [],
        expectedResultParts: [],
      };
      inPrecondition = true;
      continue;
    }

    if (!current) continue;

    // Given / And/But at the START (precondition zone)
    if (line.startsWith('Given ')) {
      current.preconditionParts.push(line.replace(/^Given\s+/i, '').trim());
      inPrecondition = true;
      continue;
    }

    // When → moves us out of precondition into steps
    if (line.startsWith('When ')) {
      inPrecondition = false;
      current.steps.push(line.replace(/^When\s+/i, '').trim());
      continue;
    }

    // Then → expected result collector (also a step)
    if (line.startsWith('Then ')) {
      inPrecondition = false;
      current.expectedResultParts.push(line.replace(/^Then\s+/i, '').trim());
      current.steps.push(line.replace(/^Then\s+/i, '').trim());
      continue;
    }

    // And / But – goes to the currently active section
    if (line.startsWith('And ') || line.startsWith('But ')) {
      const text = line.replace(/^(?:And|But)\s+/i, '').trim();
      if (inPrecondition) {
        current.preconditionParts.push(text);
      } else {
        // If we already have an expected result, collect more into it too
        if (current.expectedResultParts.length > 0) {
          current.expectedResultParts.push(text);
        }
        current.steps.push(text);
      }
    }
  }

  if (current) scenarios.push(current);

  // Build final rows
  return scenarios.map((sc, idx) => ({
    id: `TC-${String(idx + 1).padStart(3, '0')}`,
    requirementId: `REQ-${String(idx + 1).padStart(3, '0')}`,
    testCase: sc.testCase || `Test Case ${idx + 1}`,
    precondition: sc.preconditionParts.join('; ') || '—',
    steps: sc.steps.length > 0 ? sc.steps : ['(no steps found)'],
    expectedResult: sc.expectedResultParts.join('; ') || sc.steps[sc.steps.length - 1] || '—',
    // priority comes from parent; individual rows share it for now
  }));
}

// ─── Priority badge ───────────────────────────────────────────────────────────
const PriorityBadge = ({ priority }) => {
  const styles =
    priority === 'High'
      ? 'text-red-400'
      : priority === 'Medium'
      ? 'text-yellow-400'
      : 'text-green-400';
  return <span className={`font-semibold ${styles}`}>{priority}</span>;
};

// ─── Main Component ───────────────────────────────────────────────────────────
const TestCasesDisplay = ({ gherkin, priority }) => {
  if (!gherkin) return null;

  const testCases = parseGherkin(gherkin);

  // If parser produced nothing (unexpected format), fall back to raw display
  if (testCases.length === 0) {
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
      {/* Section header */}
      <h2 className="text-3xl font-bold text-white text-center mb-8 tracking-tight">
        Generated Test Cases
      </h2>

      {/* Table wrapper */}
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
            {/* Header */}
            <thead>
              <tr
                style={{
                  background: 'linear-gradient(90deg, #1e2a6e 0%, #1a237e 100%)',
                  borderBottom: '2px solid rgba(99, 132, 255, 0.3)',
                }}
              >
                {[
                  'Test Case ID',
                  'Requirement ID',
                  'Test Case',
                  'Precondition',
                  'Test Steps',
                  'Expected Result',
                  'Priority',
                ].map((col) => (
                  <th
                    key={col}
                    className="px-4 py-4 text-left text-xs font-bold uppercase tracking-wider text-blue-200"
                    style={{ whiteSpace: 'nowrap' }}
                  >
                    {col}
                  </th>
                ))}
              </tr>
            </thead>

            {/* Body */}
            <tbody>
              {testCases.map((tc, rowIdx) => (
                <tr
                  key={tc.id}
                  style={{
                    background:
                      rowIdx % 2 === 0
                        ? 'rgba(20, 30, 70, 0.6)'
                        : 'rgba(12, 20, 55, 0.5)',
                    borderBottom: '1px solid rgba(99, 132, 255, 0.1)',
                  }}
                >
                  {/* Test Case ID */}
                  <td className="px-4 py-5 text-slate-200 font-mono font-semibold align-top whitespace-nowrap">
                    {tc.id}
                  </td>

                  {/* Requirement ID */}
                  <td className="px-4 py-5 text-slate-200 font-mono align-top whitespace-nowrap">
                    {tc.requirementId}
                  </td>

                  {/* Test Case description */}
                  <td className="px-4 py-5 text-slate-100 align-top max-w-[180px]">
                    {tc.testCase}
                  </td>

                  {/* Precondition */}
                  <td className="px-4 py-5 text-slate-300 align-top max-w-[200px]">
                    {tc.precondition}
                  </td>

                  {/* Test Steps – auto-numbered */}
                  <td className="px-4 py-5 text-slate-300 align-top max-w-[220px]">
                    <ol className="list-none space-y-1">
                      {tc.steps.map((step, i) => (
                        <li key={i} className="flex gap-2">
                          <span className="text-blue-400 font-semibold shrink-0">{i + 1}.</span>
                          <span>{step}</span>
                        </li>
                      ))}
                    </ol>
                  </td>

                  {/* Expected Result */}
                  <td className="px-4 py-5 text-slate-300 align-top max-w-[180px]">
                    {tc.expectedResult}
                  </td>

                  {/* Priority */}
                  <td className="px-4 py-5 align-top whitespace-nowrap">
                    <PriorityBadge priority={priority} />
                  </td>
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
