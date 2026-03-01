import React from 'react';

const MatrixPanel = ({ userStory, testCases, priority }) => {
    if (!userStory || !testCases) return null;

    // Simple parsing of Gherkin to count scenarios for the matrix
    const scenarios = testCases.split('Scenario:').filter(s => s.trim()).length || 1;

    // ID Generation (Mock)
    const reqId = "REQ-" + Math.floor(Math.random() * 1000);
    const tcIdPrefix = "TC-" + Math.floor(Math.random() * 1000);

    return (
        <div className="mt-8">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2 mb-6">
                <span className="w-1 h-8 bg-purple-500 rounded-full"></span>
                Traceability Matrix
            </h2>

            <div className="glass-panel rounded-xl overflow-hidden shadow-2xl bg-slate-900/50 backdrop-blur-md border border-slate-700">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-800/80 text-slate-300 text-sm uppercase tracking-wider">
                                <th className="p-4 font-semibold border-b border-slate-700">Req ID</th>
                                <th className="p-4 font-semibold border-b border-slate-700">User Story Snippet</th>
                                <th className="p-4 font-semibold border-b border-slate-700">Test Case ID</th>
                                <th className="p-4 font-semibold border-b border-slate-700">Priority</th>
                                <th className="p-4 font-semibold border-b border-slate-700">Status</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-700/50">
                            {Array.from({ length: scenarios }).map((_, idx) => (
                                <tr key={idx} className="hover:bg-white/5 transition-colors text-slate-300">
                                    <td className="p-4 font-mono text-blue-400">{reqId}</td>
                                    <td className="p-4 truncate max-w-xs" title={userStory}>
                                        {userStory.substring(0, 50)}...
                                    </td>
                                    <td className="p-4 font-mono text-purple-400">{tcIdPrefix}-{idx + 1}</td>
                                    <td className="p-4">
                                        <span className={`px-2 py-1 rounded text-xs font-bold ${priority === 'High' ? 'bg-red-500/20 text-red-400' :
                                                priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                                    'bg-green-500/20 text-green-400'
                                            }`}>
                                            {priority || 'Formulating'}
                                        </span>
                                    </td>
                                    <td className="p-4">
                                        <span className="flex items-center gap-1.5 text-green-400 text-sm font-medium">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                            Covered
                                        </span>
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

export default MatrixPanel;
