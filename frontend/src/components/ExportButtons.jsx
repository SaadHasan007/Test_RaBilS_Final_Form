import React from 'react';
import jsPDF from 'jspdf';

const ExportButtons = ({ testCases, userStory }) => {
    const handleExportCSV = () => {
        const csvContent = "data:text/csv;charset=utf-8,"
            + "User Story,Test Cases\n"
            + `"${userStory.replace(/"/g, '""')}","${testCases.replace(/"/g, '""')}"`;

        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "test_cases.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const handleExportPDF = () => {
        const doc = new jsPDF();

        doc.setFontSize(16);
        doc.text("Test Case Report", 20, 20);

        doc.setFontSize(12);
        doc.text(`User Story:`, 20, 30);

        // Split text to fit page
        const splitUserStory = doc.splitTextToSize(userStory, 170);
        doc.text(splitUserStory, 20, 40);

        let yPos = 40 + (splitUserStory.length * 7) + 10;

        doc.text("Generated Test Cases (Gherkin):", 20, yPos);
        yPos += 10;

        doc.setFont("courier");
        doc.setFontSize(10);
        const splitTestCases = doc.splitTextToSize(testCases, 170);
        doc.text(splitTestCases, 20, yPos);

        doc.save("test_cases.pdf");
    };

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
