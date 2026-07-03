import React, { useState } from 'react';

const AmbiguityCheck = ({ ambiguityNotes, formattedStory, usedAi, originalStory }) => {
    const [showNotes, setShowNotes] = useState(true);

    // handle this error ambiguity notes are not string but a list of strings
    // if (Array.isArray(ambiguityNotes)) {
    //     ambiguityNotes = ambiguityNotes.join('\n');
    // }

    // Nothing to show if no data has arrived yet
    if (!formattedStory && (!ambiguityNotes || ambiguityNotes.length === 0)) return null;

    const hasChanges = formattedStory && formattedStory.trim() !== originalStory?.trim();
    const hasNotes = ambiguityNotes && ambiguityNotes.length > 0;

    return (
        <div className="mt-6 space-y-4 animate-fade-in-up">

            {/* ── Formatted Story Card ── */}
            {formattedStory && (
                <div className="p-5 rounded-2xl bg-emerald-900/20 border border-emerald-500/30">
                    <div className="flex items-center gap-2 mb-3">
                        {/* Checkmark icon */}
                        <svg className="h-5 w-5 text-emerald-400 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        <h3 className="text-sm font-semibold text-emerald-300 uppercase tracking-wider">
                            {usedAi ? 'AI-Formatted User Story' : 'Your User Story'}
                        </h3>
                        {usedAi && (
                            <span className="ml-auto text-xs font-medium px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30">
                                GPT‑3.5
                            </span>
                        )}
                    </div>
                    <pre className="text-slate-200 text-sm leading-7 font-mono whitespace-pre-wrap bg-slate-900/50 rounded-xl px-5 py-4 border border-white/5">
                        {formattedStory}
                    </pre>
                    {hasChanges && (
                        <p className="mt-2 text-xs text-slate-400">
                            ✦ The story above was rewritten from your input. It will be sent to the test case generator.
                        </p>
                    )}
                </div>
            )}

            {/* ── Ambiguity Notes ── */}
            {hasNotes && (
                <div className="rounded-2xl bg-yellow-900/20 border border-yellow-500/30 overflow-hidden">
                    <button
                        onClick={() => setShowNotes(prev => !prev)}
                        className="w-full flex items-center gap-2 px-5 py-3 text-left hover:bg-yellow-900/20 transition-colors"
                    >
                        {/* Warning icon */}
                        <svg className="h-5 w-5 text-yellow-400 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                        <h3 className="text-sm font-semibold text-yellow-300 uppercase tracking-wider flex-1">
                            {ambiguityNotes.length} Ambiguit{ambiguityNotes.length > 1 ? 'ies' : 'y'} {usedAi ? 'Resolved' : 'Detected'}
                        </h3>
                        {/* Chevron */}
                        <svg
                            className={`h-4 w-4 text-yellow-400 transition-transform duration-200 ${showNotes ? 'rotate-180' : ''}`}
                            viewBox="0 0 20 20" fill="currentColor"
                        >
                            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                        </svg>
                    </button>

                    {showNotes && (
                        <ul className="px-5 pb-4 space-y-2">
                            {ambiguityNotes.map((note, i) => (
                                <li key={i} className="flex items-start gap-2 text-sm text-yellow-200/80">
                                    <span className="mt-0.5 text-yellow-500 flex-shrink-0">›</span>
                                    {note}
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
        </div>
    );
};

export default AmbiguityCheck;
