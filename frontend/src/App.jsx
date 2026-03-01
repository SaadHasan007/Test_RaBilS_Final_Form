import React, { useState } from 'react';
import UserStoryInput from './components/UserStoryInput';
import AmbiguityCheck from './components/AmbiguityCheck';
import TestCasesDisplay from './components/TestCasesDisplay';
import ExportButtons from './components/ExportButtons';
import MatrixPanel from './components/MatrixPanel';
import StatusBadge from './components/StatusBadge';
import { checkAmbiguity, generateTestCases } from './services/api';

function App() {
  const [userStory, setUserStory] = useState('');

  // Ambiguity check state
  const [formattedStory, setFormattedStory] = useState(null);
  const [ambiguityNotes, setAmbiguityNotes] = useState([]);
  const [usedAi, setUsedAi] = useState(false);
  const [ambiguityLoading, setAmbiguityLoading] = useState(false);

  // Generation state
  const [gherkin, setGherkin] = useState('');
  const [priority, setPriority] = useState('');
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const [error, setError] = useState(null);

  // ── Step 1: Check & format ambiguity ──────────────────────────────────────
  const handleCheckAmbiguity = async () => {
    if (!userStory.trim()) {
      setError('Please enter a user story first.');
      return;
    }
    setError(null);
    setAmbiguityLoading(true);
    setFormattedStory(null);
    setAmbiguityNotes([]);
    setShowResults(false);

    try {
      const result = await checkAmbiguity(userStory);
      setFormattedStory(result.formatted_story);
      setAmbiguityNotes(result.ambiguity_notes || []);
      setUsedAi(result.used_ai || false);
    } catch (err) {
      setError('Ambiguity check failed. Please make sure the backend is running.');
    } finally {
      setAmbiguityLoading(false);
    }
  };

  // ── Step 2: Generate test cases using the formatted story ─────────────────
  const handleGenerate = async () => {
    if (!userStory.trim()) {
      setError('Please enter a user story first.');
      return;
    }
    setError(null);
    setLoading(true);
    setShowResults(false);

    try {
      // Pass formattedStory so the backend uses the cleaned version
      const result = await generateTestCases(userStory, formattedStory);
      setGherkin(result.gherkin);
      setPriority(result.priority);
    } catch (err) {
      setError('Failed to generate test cases.');
      setLoading(false);
    }
    // setLoading(false) is NOT called here — StatusBadge calls onComplete when its
    // animation finishes, which then calls handleAnimationComplete below.
  };

  const handleAnimationComplete = () => {
    setLoading(false);
    setShowResults(true);
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8 font-sans selection:bg-pink-500 selection:text-white">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-16 relative">
          <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl pointer-events-none"></div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-4">
            <span className="text-gradient">Test RaBilS</span>
          </h1>
        </div>

        <div className="glass-panel rounded-3xl overflow-hidden p-1">
          <div className="bg-slate-900/50 p-8 sm:p-10 rounded-[1.3rem]">

            <UserStoryInput value={userStory} onChange={(val) => {
              setUserStory(val);
              // Reset ambiguity results when the story is edited
              setFormattedStory(null);
              setAmbiguityNotes([]);
            }} />

            {error && (
              <div className="mb-6 p-4 text-red-200 bg-red-900/30 border border-red-500/30 rounded-xl flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
                {error}
              </div>
            )}

            {/* ── Action buttons ── */}
            <div className="flex flex-col sm:flex-row gap-4 mt-8 justify-center">

              {/* Step 1 button: Check & Format */}
              <button
                onClick={handleCheckAmbiguity}
                disabled={ambiguityLoading || loading}
                className="w-full sm:w-1/3 px-6 py-4 font-bold rounded-2xl text-lg disabled:opacity-50 disabled:cursor-not-allowed
                           bg-yellow-500/10 border border-yellow-500/40 text-yellow-300
                           hover:bg-yellow-500/20 transition-all duration-200"
              >
                {ambiguityLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                    </svg>
                    Checking…
                  </span>
                ) : '🔍 Check Ambiguity'}
              </button>

              {/* Step 2 button: Generate */}
              <button
                onClick={handleGenerate}
                disabled={loading || ambiguityLoading}
                className="w-full sm:w-2/3 px-6 py-4 btn-primary font-bold rounded-2xl text-lg disabled:opacity-50 disabled:cursor-not-allowed group shadow-blue-900/50"
              >
                ⚡ Generate Test Cases
              </button>
            </div>

            <StatusBadge isProcessing={loading} onComplete={handleAnimationComplete} />

            {/* Ambiguity results (formatted story + notes) */}
            <AmbiguityCheck
              ambiguityNotes={ambiguityNotes}
              formattedStory={formattedStory}
              usedAi={usedAi}
              originalStory={userStory}
            />

            {showResults && gherkin && (
              <div className="animate-fade-in-up mt-10 border-t border-white/5 pt-10">
                <TestCasesDisplay gherkin={gherkin} priority={priority} />
                {/* Use formattedStory for the matrix if available */}
                <MatrixPanel
                  userStory={formattedStory || userStory}
                  testCases={gherkin}
                  priority={priority}
                />
                <ExportButtons testCases={gherkin} userStory={formattedStory || userStory} />
              </div>
            )}
          </div>
        </div>

        <div className="mt-12 text-center text-slate-500 text-sm font-medium">
          &copy; {new Date().getFullYear()} Test RaBilS. <span className="text-slate-600">|</span> Made By: Saad, Rafi &amp; Bilal ❤
        </div>
      </div>
    </div>
  );
}

export default App;
