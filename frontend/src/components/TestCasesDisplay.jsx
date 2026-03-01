import React from 'react';

const TestCasesDisplay = ({ gherkin, priority }) => {
    if (!gherkin) return null;

    const priorityColor =
        priority === 'High' ? 'text-red-400 bg-red-500/10 border-red-500/20' :
            priority === 'Medium' ? 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20' :
                'text-green-400 bg-green-500/10 border-green-500/20';

    return (
        <div className="mt-8">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span className="w-1 h-8 bg-blue-500 rounded-full"></span>
                    Generated Test Cases
                </h2>
                {priority && (
                    <span className={`px-4 py-1.5 rounded-full text-sm font-semibold border ${priorityColor} backdrop-blur-md`}>
                        Priority: {priority}
                    </span>
                )}
            </div>

            <div className="relative rounded-xl overflow-hidden shadow-2xl bg-slate-900 border border-slate-800 group">
                <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                        onClick={() => navigator.clipboard.writeText(gherkin)}
                        className="text-xs uppercase font-bold text-slate-500 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-lg transition-colors border border-slate-700"
                    >
                        Copy
                    </button>
                </div>
                <div className="flex items-center px-4 py-3 bg-slate-900 border-b border-slate-800">
                    <div className="flex space-x-2">
                        <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                        <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
                    </div>
                    <div className="ml-4 text-xs text-slate-500 font-mono">feature.feature</div>
                </div>
                <pre className="p-6 overflow-x-auto bg-slate-900/50">
                    <code className="text-blue-100 font-mono text-sm leading-relaxed block">
                        {gherkin}
                    </code>
                </pre>
            </div>
        </div>
    );
};

export default TestCasesDisplay;
