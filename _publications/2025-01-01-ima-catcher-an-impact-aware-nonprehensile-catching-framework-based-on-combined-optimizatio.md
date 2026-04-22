---
title: "IMA-catcher: An IMpact-aware nonprehensile catching framework based on combined optimization and learning"
collection: publications
category: manuscripts
permalink: /publication/ima-catcher-an-impact-aware-nonprehensile-catching-framework-based-on-combined-optimizatio
excerpt: '<p>Robotic catching of flying objects typically generates high-impact forces that might lead to task failure and potential hardware damages. This is accentuated when the object mass to robot payload ratio increases, give'
date: 2025-01-01
venue: 'The International Journal of Robotics Research'
paperurl: 'https://doi.org/10.1177/02783649251345851'
citation: 'Francesco Tassi; Jianzhuang Zhao; Gustavo JG Lahr; Luna Gava; Marco Monforte; Arren Glover; Chiara Bartolozzi; Arash Ajoudani (2025). &quot;IMA-catcher: An IMpact-aware nonprehensile catching framework based on combined optimization and learning.&quot; <i>The International Journal of Robotics Research</i>.'
---

<p>Robotic catching of flying objects typically generates high-impact forces that might lead to task failure and potential hardware damages. This is accentuated when the object mass to robot payload ratio increases, given the strong inertial components characterizing this task. This paper aims to address this problem by proposing an implicitly impact-aware framework that accomplishes the catching task in both pre- and post-catching phases. In the first phase, a motion planner generates optimal trajectories that minimize catching forces, while in the second, the object’s energy is dissipated smoothly, minimizing bouncing. In particular, in the pre-catching phase, a real-time optimal planner is responsible for generating trajectories of the end-effector that minimize the velocity difference between the robot and the object to reduce impact forces during catching. In the post-catching phase, the robot’s position, velocity, and stiffness trajectories are generated based on human demonstrations when catching a series of free-falling objects with unknown masses. A hierarchical quadratic programming-based controller is used to enforce the robot’s constraints (i.e., joint and torque limits) and create a stack of tasks that minimizes the reflected mass at the end-effector as a secondary objective. The initial experiments isolate the problem along one dimension to accurately study the effects of each contribution on the metrics proposed. We show how the same task, without velocity matching, would be infeasible due to excessive joint torques resulting from the impact. The addition of reflected mass minimization is then investigated, and the catching height is increased to evaluate the method’s robustness. Finally, the setup is extended to catching along multiple Cartesian axes, to prove its generalization in space.</p>

Authors: Francesco Tassi; Jianzhuang Zhao; Gustavo JG Lahr; Luna Gava; Marco Monforte; Arren Glover; Chiara Bartolozzi; Arash Ajoudani

Venue: The International Journal of Robotics Research (2025)
DOI: 10.1177/02783649251345851

[Access paper here](https://doi.org/10.1177/02783649251345851){:target="_blank"}
