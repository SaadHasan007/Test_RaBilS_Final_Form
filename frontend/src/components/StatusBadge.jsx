import React, { useEffect, useState } from 'react';

const steps = [
    "Ambiguity Detecting",
    "Ambiguity Detected",
    "Ambiguity Removing",
    "Test Case Generating",
    "Test Case Optimizing",
    "Finalizing Test Cases"
];

const StatusBadge = ({ isProcessing, onComplete }) => {
    const [currentStep, setCurrentStep] = useState(0);

    useEffect(() => {
        if (isProcessing) {
            setCurrentStep(0);
            const interval = setInterval(() => {
                setCurrentStep((prev) => {
                    if (prev < steps.length - 1) {
                        return prev + 1;
                    } else {
                        clearInterval(interval);
                        if (onComplete) onComplete();
                        return prev;
                    }
                });
            }, 800); // 800ms per step to visualize the flow
            return () => clearInterval(interval);
        }
    }, [isProcessing, onComplete]);

    if (!isProcessing && currentStep === 0) return null;

    return (
        <div className="flex flex-col items-center justify-center my-6 space-y-2">
            <div className="flex items-center gap-3 bg-slate-800/80 px-6 py-3 rounded-full border border-slate-700 shadow-xl backdrop-blur-md">
                <div className="relative">
                    <div className="w-3 h-3 bg-blue-500 rounded-full animate-ping absolute"></div>
                    <div className="w-3 h-3 bg-blue-500 rounded-full relative"></div>
                </div>
                <span className="text-blue-100 font-mono text-sm uppercase tracking-widest">
                    {steps[currentStep]}...
                </span>
            </div>
            <div className="w-full max-w-xs bg-slate-800 rounded-full h-1.5 mt-2 overflow-hidden">
                <div
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-1.5 rounded-full transition-all duration-300 ease-out"
                    style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                ></div>
            </div>
        </div>
    );
};

export default StatusBadge;
