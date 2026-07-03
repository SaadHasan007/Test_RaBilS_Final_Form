import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Calls /api/ambiguity.
 * Returns: { formatted_story, ambiguity_notes, used_ai }
 */
export const removeAmbiguity = async (userStory, ambiguityReport) => {
  try {
    console.log("this line executed api.js ~line 11");
    const response = await axios.post(`${API_BASE_URL}/ambiguityRemove`, {
      user_story: userStory,
      ambiguity_report: ambiguityReport
    });
    console.log("this line executed api.js ~line 14",userStory, ambiguityReport);
    console.log("this line executed api.js ~line 15", response.data);
    return response.data;
  } catch (error) {
    console.error('Error removing ambiguity:api.js line 16', error);
    console.log("this line executed api.js ~line 17");
    throw error;
  }
};

export const checkAmbiguity = async (userStory) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/ambiguityReport`, {
      user_story: userStory,
    });
    return response.data;
  } catch (error) {
    console.error('Error checking ambiguity:api.js line 28', error);
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
    console.error('Error generating test cases: api.js line 36', error);
    throw error;
  }
};


export const getTestCaseList = async () =>{
  try{
    const response = await axios.get(`${API_BASE_URL}/testcase_list`);
    return response.data;
  } catch (error) {
    console.error('Error fetching testcases: api.js ~47', error);
    throw error;
  }
};

export const emptyTestCaseList = async () =>{
  try{
    await axios.delete(`${API_BASE_URL}/testcase_list`);
  } catch (error) {
    console.error('Error clearing list: api.js ~56', error);
    throw error;
  }
};

export const getDublicateTestCases = async (userStory) =>{
  try{
    const response = await axios.post(`${API_BASE_URL}`/dublicates, {
      user_story: userStory,
    });
    return response.data;
  }catch (error) {
    console.error('Error identifying dublicates: api.js ~65', error);
    throw error;
  }
};