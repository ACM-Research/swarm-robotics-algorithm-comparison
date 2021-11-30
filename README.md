# Comparison of Swarm Robotics Algorithms
Explore algorithms that use swarm robotics concepts to accomplish difficult tasks, implement such algorithms, and compare the speed and accuracy of these algorithms when competing in various tasks like moving across an environment with obstacles and collecting items throughout an environment.

# Introduction
Swarm algorithms are a problem solving tool that utilize many decentralized, often homogenous agents to accomplish a global or local task. Successful swarm algorithms are fabricated into robots that have real-world uses. Nearly all swarm algorithms are based on nature. A decentralized swarm is both scalable and robust. That is, the system performs well for varying quantities of agents and is immune to failure. Expectedly, there are drawbacks such as the difficulty of predicted the global behavior. 
One such application of swarm robotics is to aggregate resources in an unknown environment into piles. Our project explores the optimal algorithm to do this task. We compare the performance of two different swarm algorithms: cockroach and pheromone.

# Methodology
We used the Unreal Engine to run simulations. Each algorithm was tested on a flat and a hilly map with obstacles. Within each map, we ran simulations using 30 and 60 bots and 50, 100, and 150 resources. 
Multiple samples for each trial (i.e. cockroach algorithm on flat map with 30 robots and 50 resources) were collected. For each trial, the location of each resource was tracked with respect to time 
The performance of the algorithms were measured using the DBSCAN algorithm, which calculates the amount of non clustered resources over time. 

# Analysis
For the pheromone algorithm, the non clustered resources generally decrease over time at a steady rate. For the cockroach algorithm, the number of non clustered resources is generally volatile sometimes decreases. 
Universally, the number of non clustered resources tend to decrease over time, meaning the bots are successfully aggregating resources into clusters. The data has relatively high variation between trials, but overall, the pheromone algorithm performs better than the cockroach. 
Additionally, the algorithms perform better on the flat map compared to the hilly map. Finally, the simulations with more robots outperform simulations with fewer robots most of the time.

# Conclusion
Our research applies to problems such as real-world mining and search/rescue. The environments we used were somewhat limited in their scope. Future research can test on different terrains and make use of non-homogeneous bots to test variations of popular algorithms. This will increase the amount and complexity of problems these algorithms can tackle.

# Contributors
- [Ryan Aspenleiter](https://github.com/RyanAspen) - Research Lead
- [Dr. Ovidiu Daescu](https://personal.utdallas.edu/~daescu/) - Faculty Advisor

# Code
To see the code, go to the pheromone branch.
