import React from "react";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

const ExportButtons = ({ testCases, userStory }) => {
  // temporary used sample test case , becoz this function only works with strings,
  // handle this error so that it can handle list of test cases
//   userStory = "as a user i want <something> so that <some benefit>";
//   testCases =
//     "testCaseId : tc_001 \n requirementId: req_id \n testCase : test case \n precondition: precondition \n steps \n step 1 \n step 2 \n step 3 \n expectedResult : expected result \n priority: high";

  // const handleExportCSV = () => {
  //     const csvContent = "data:text/csv;charset=utf-8,"
  //         + "User Story,Test Cases\n"
  //         + `"${userStory.replace(/"/g, '""')}","${testCases.replace(/"/g, '""')}"`;

  //     const encodedUri = encodeURI(csvContent);
  //     const link = document.createElement("a");
  //     link.setAttribute("href", encodedUri);
  //     link.setAttribute("download", "test_cases.csv");
  //     document.body.appendChild(link);
  //     link.click();
  //     document.body.removeChild(link);
  // };
  const handleExportCSV = () => {
    if (!testCases || testCases.length === 0) return;

    const headers = [
      "TestCaseId",
      "RequirementId",
      "TestCase",
      "Precondition",
      "Steps",
      "ExpectedResult",
      "Priority",
    ];

    const rows = testCases.map((tc) => [
      tc.testCaseId,
      tc.requirementId,
      tc.testCase,
      tc.precondition,
      tc.steps.join(" | "), // convert array → string
      tc.expectedResult,
      tc.priority,
    ]);

    const csvContent =
      "data:text/csv;charset=utf-8," +
      [headers, ...rows]
        .map((row) =>
          row.map((val) => `"${String(val).replace(/"/g, '""')}"`).join(","),
        )
        .join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "test_cases.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
const handleExportPDF = () => {
    if (!testCases || testCases.length === 0) return;

    const doc = new jsPDF();

    doc.setFontSize(16);
    doc.text("Test Case Report", 14, 15);

    doc.setFontSize(11);
    doc.text(`User Story: ${userStory}`, 14, 25);

    const tableColumn = [
        "TC ID",
        "REQ ID",
        "Test Case",
        "Precondition",
        "Steps",
        "Expected",
        "Priority"
    ];

    const tableRows = testCases.map(tc => [
        tc.testCaseId,
        tc.requirementId,
        tc.testCase,
        tc.precondition,
        tc.steps.join("\n"), // multiline in PDF
        tc.expectedResult,
        tc.priority
    ]);

    autoTable(doc, {
        startY: 35,
        head: [tableColumn],
        body: tableRows,
        styles: { fontSize: 8 },
    });

    doc.save("test_cases.pdf");
};

    // const handleExportPDF = () => {
    //   const doc = new jsPDF();

    //   doc.setFontSize(16);
    //   doc.text("Test Case Report", 20, 20);

    //   doc.setFontSize(12);
    //   doc.text(`User Story:`, 20, 30);

    //   // Split text to fit page
    //   const splitUserStory = doc.splitTextToSize(userStory, 170);
    //   doc.text(splitUserStory, 20, 40);

    //   let yPos = 40 + splitUserStory.length * 7 + 10;

    //   doc.text("Generated Test Cases (Gherkin):", 20, yPos);
    //   yPos += 10;

    //   doc.setFont("courier");
    //   doc.setFontSize(10);
    //   const splitTestCases = doc.splitTextToSize(testCases, 170);
    //   doc.text(splitTestCases, 20, yPos);

    //   doc.save("test_cases.pdf");
    // };

  if (!testCases) return null;

  return (
    <div className="flex gap-4 mt-6">
      <button
        onClick={handleExportCSV}
        className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg shadow transition-colors"
      >
        Export CSV
      </button>
      <button
        onClick={handleExportPDF}
        className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg shadow transition-colors"
      >
        Export PDF
      </button>
    </div>
  );
};

export default ExportButtons;
