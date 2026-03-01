import React from 'react';

const UserStoryInput = ({ value, onChange }) => {
    return (
        <div className="mb-6 relative">
            <label htmlFor="userStory" className="block text-sm font-semibold text-slate-300 mb-3 ml-1 uppercase tracking-wider">
                Input User Story
            </label>
            <div className="relative group">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                <textarea
                    id="userStory"
                    rows="5"
                    className="relative w-full px-6 py-5 rounded-xl bg-slate-800 text-slate-100 border border-slate-700/50 focus:border-blue-500/50 focus:ring-0 shadow-xl placeholder-slate-500 transition-all resize-none text-lg leading-relaxed"
                    placeholder="As a user, I want to login securely so that I can access my personalized dashboard..."
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                />
            </div>
        </div>
    );
};

export default UserStoryInput;
