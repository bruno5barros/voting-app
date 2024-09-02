Let's first highlight the features that need to be developed based on the requirements. Then, I'll explain each feature in detail.

### **Highlighted Features:**

1. **Everyone can add/remove/update restaurants.** DONE
2. **Every user gets X (hardcoded, but "configurable") votes per day.** DONE
3. **Each vote has a "weight". First user vote on the same restaurant counts as 1, second as 0.5, 3rd and all subsequent votes as 0.25.** DONE
4. **If a voting result is the same on multiple restaurants, the winner is the one who got more distinct users to vote on it.** DONE
5. **Every day vote amounts are reset. Unused previous day votes are lost.** DONE
6. **Show the history of selected restaurants per time period.** DONE
7. **Frontend dev will need a way to show which restaurants users can vote on and which restaurant is a winner.** DONE
8. **README on how to use the API, launch the project, etc.**

### **Detailed Explanation of Each Feature:**

#### 1. **Everyone can add/remove/update restaurants.** DONE
   - **Add Restaurant:**
     - Implement functionality that allows any user to add a new restaurant to the list of options. This involves creating an endpoint where users can submit restaurant details (e.g., name, description).
   - **Update Restaurant:**
     - Provide functionality to update existing restaurant details. Users should be able to modify the name, description, or other relevant information of a restaurant.
   - **Remove Restaurant:**
     - Allow users to delete a restaurant from the list. This feature is crucial to manage the list and remove outdated or irrelevant entries.

#### 2. **Every user gets X (hardcoded, but "configurable") votes per day.** DONE
   - **Voting Limits:**
     - Implement a system that restricts each user to a specific number of votes per day (X). This value should be configurable, allowing easy adjustment if needed. Once a user has used up their daily quota, they should not be able to vote again until the next day.

#### 3. **Each vote has a "weight". First user vote on the same restaurant counts as 1, second as 0.5, 3rd and all subsequent votes as 0.25.** DONE
   - **Vote Weighting System:**
     - Implement a system where the weight of each vote decreases if the user votes for the same restaurant multiple times. The first vote counts as 1 point, the second as 0.5 points, and any subsequent votes as 0.25 points. This encourages users to spread their votes across different options.

#### 4. **If a voting result is the same on multiple restaurants, the winner is the one who got more distinct users to vote on it.**
   - **Tie-Breaker Logic:**
     - Implement logic to handle tie situations where two or more restaurants have the same total vote weight. The restaurant with votes from the most distinct users should be declared the winner. This ensures fairness in the voting process.

#### 5. **Every day vote amounts are reset. Unused previous day votes are lost.** DONE
   - **Daily Vote Reset:**
     - Implement a system that resets all votes at the end of each day. Users' unused votes do not carry over to the next day, ensuring a fresh start each day. This reset can be automated to occur at a specific time or triggered manually.

#### 6. **Show the history of selected restaurants per time period.**
   - **Voting History Tracking:**
     - Implement a feature that tracks and stores the voting history, allowing users to see which restaurant won on any given day. This historical data can be queried based on specific time periods, providing insights into past voting trends.

#### 7. **Frontend dev will need a way to show which restaurants users can vote on and which restaurant is a winner.**
   - **Expose Restaurant and Winner Data via API:**
     - Provide an endpoint that lists all available restaurants for voting. Additionally, create an endpoint that shows the daily winner, allowing the frontend to display this information to users.

#### 8. **README on how to use the API, launch the project, etc.**
   - **Documentation:**
     - Write a detailed README file that explains how to set up and run the project. Include information on how to interact with the API, a description of the endpoints, and examples of usage. This documentation ensures that other developers can easily understand and use the API.

### **Summary**

Each of these highlighted features represents a crucial part of the voting REST API for lunch destination selection. Implementing these features will ensure the API meets all the specified requirements, provides a robust and fair voting system, and offers clear, accessible documentation for developers.



