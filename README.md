## YouTube Data Harvesting and Warehousing

### Problem Statement:
The goal is to create a Streamlit application for harvesting and analyzing data from YouTube channels. Key features include:

- Retrieve channel details (subscribers, video count, etc.) using YouTube API.
- Store data in MongoDB as a data lake.
- Migrate data to SQL database for analysis.

### Approach:
1. **Set up Streamlit app**: Create a UI for user interaction.
2. **Connect to YouTube API**: Retrieve channel and video data.
3. **Store data in MongoDB**: Use MongoDB for flexible data storage.
4. **Query SQL database**: Perform analysis on stored data.
5. **Visualize results**: Display insights using Streamlit's visualization features.

### How to Use:
1. Enter YouTube Channel IDs.
2. Extract data or save to MongoDB.
3. Analyze stored data through predefined questions.
4. View trends via charts and tables.

### Workflow and Execution:
1. **Setup:**
   - Ensure Python and necessary libraries are installed.
   - Clone the project repository from GitHub.

2. **Environment Setup:**
   - Set up a virtual environment to manage dependencies.
   - Install required Python libraries.
   
3. **Data Collection:**
   - Run the Streamlit app (`Youtube_Harvesting.py`).
   - Input YouTube Channel IDs to extract data.
   - Optionally, save data to MongoDB.

4. **Data Processing:**
   - Utilize Google API for fetching channel and video details.
   - Store data in MongoDB collections (`channel_details`, `video_details`, `comments_details`).
   
5. **Accessing Information:**
   - Use Streamlit UI to access various queries and analyses.
   - Select predefined questions to retrieve insights from MongoDB.
   
6. **Migration to SQL:**
   - Implement migration script to transfer data from MongoDB to SQL database.
   - Create SQL tables to store channel and video information.
   
7. **Querying SQL Database:**
   - Execute SQL queries to perform more structured analysis.
   - Join tables and aggregate data for deeper insights.

8. **Visualization:**
   - Use Streamlit's data visualization capabilities to present results.
   - Generate charts and graphs to illustrate trends and patterns.

9. **Documentation and Reporting:**
   - Update README with detailed project description, instructions, and workflow.
   - Provide clear documentation for codebase and functionalities.
   - Prepare a report summarizing project objectives, methodologies, and findings.

10. **Deployment:**
    - Optionally, deploy the Streamlit app on hosting platforms like Heroku or Streamlit Sharing.
    - Ensure proper configuration and environment setup for seamless deployment.

11. **Maintenance and Updates:**
    - Monitor API changes and update code accordingly.
    - Address bug fixes and feature requests as needed.
    - Document changes and maintain version control for future enhancements.

For detailed instructions, refer to the respective sections in the Streamlit app.
