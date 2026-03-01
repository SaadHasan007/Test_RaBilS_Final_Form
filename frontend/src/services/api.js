import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Calls /api/ambiguity.
 * Returns: { formatted_story, ambiguity_notes, used_ai }
 */
export const checkAmbiguity = async (userStory) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/ambiguity`, {
      user_story: userStory,
    });
    return response.data;
  } catch (error) {
    console.error('Error checking ambiguity:', error);
    throw error;
  }
};

/**
 * Calls /api/generate.
 * Pass formattedStory (from the ambiguity step) so the model uses the
 * cleaned-up version instead of raw input.
 * Returns: { gherkin, priority }
 */
export const generateTestCases = async (userStory, formattedStory = null) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate`, {
      user_story: userStory,
      formatted_story: formattedStory,
    });
    return response.data;
  } catch (error) {
    console.error('Error generating test cases:', error);
    throw error;
  }
};
