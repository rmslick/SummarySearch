# **SummarySearch**

### Overview
`SummarySearch` This project demonstrates the ability to cluster data on a NOSQL database using senitment analysis and abstractive text summarzation techniques.  Included is a user interface which connects the user to a host of functions which can connect current issues to previous lessons learned an attempt to perform risk analysis given sentimetns of prior lessons learned and current project proposals was attempted but proved unreliable.  Additionally there is a graphical user interface developed in html css and JS which allows users to see how our functionality may be used.
Sentiment analysis followed from SBERT: https://arxiv.org/pdf/1908.10084.pdf using pytorch and extractive summary followed from https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html both of which underpin all search related functionality.
![alt text](https://user-images.githubusercontent.com/30224178/92985860-886e1e80-f484-11ea-96c0-f172973d1a26.PNG)
                                                  Current home page of web page UI 

![alt text](https://user-images.githubusercontent.com/30224178/92985856-84420100-f484-11ea-8b0f-16e5f9454596.PNG)

![alt text](https://user-images.githubusercontent.com/30224178/92985862-8a37e200-f484-11ea-8991-677d46ec722a.PNG)
                                Smart search feature in web page before and after submitting sample text 
#### Methods

- SummarizeEntry(self, fullBody) - Using Google's t5 extractive summary algorithm  perorm an abstractive summary on a user query. Used to project prior lessons learned on furutre projects given a description

- RiskAnalsys(ProjectDescription): Attain a risk level given a project descritpion using the group of clustered lessons learned on our database and their risk sentiments.  (Unfinished, needs better sentiment analyzer)

- GroupingAlgorithm() - Iterates over database and creates groups automatically based on equivalence relations wherein the relation is a seimilarity ranking obtained through sentiment analysis.  From these groups monitoring tools can be devised such as rate of growth to understand where problems are arising.

- BasicSearch(dict): Takes input fields and performs basic matching search on database for lessons
-Graph(LessonLearned): Take in lesson learned and graph other lessons based on sentiment ranking from corpus

#### Dependencies
- MongoDB
    - `NoSql database to hold lessons learned and corpus`
- PyMongo:
    - `For scripting and access to database collections.  Functionality is included to init, add and remove entires to the DB.`
- PyTorch and t5
    - `For extractive summaries`
- transformers
    - `For SBERT sentiment analysis`
- Python3.8


#### File Structure
The basic structure is similar to all Aeon nodes in the architecture

| File Name | Description |
| ----------- | ----------- |
| `DBFill` 			| Helper method to fill mongoDB with lessons learned using pymongo. |
| `DatabaseInterface` 			| Contains all  user functions to perform smart searches, database clustering algorithms and . |


