import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

class Planner:
  def __init__(self, node_name='planner', n_robots=1):
    rospy.init_node(node_name)
    self.rate = rospy.Rate(1)

    self.n_robots = n_robots
    self.odoms = [None] * n_robots
    self.states = [None] * n_robots
    self.clear_goals_svcs = []
    self.add_goal_svcs = []

    for r_i in range(n_robots):
      robot_ns = '/robot_%02/' % r_i
      rospy.Subscriber(robot_ns + 'odometry', Odometry, self.curry(i, self.odom_callback), queue_size=1)
      rospy.Subscriber(robot_ns + 'control_state', String, self.curry(i, self.ctrl_state_callback), queue_size=1)
      self.clear_goals_svcs.append(rospy.ServiceProxy(robot_ns + 'clear_goals', ClearGoals))
      self.add_goal_svcs.append(rospy.ServiceProxy(robot_ns + 'add_goal', AddGoal))

  def curry(self, func, idx):
    return lambda x : func(x, idx)

  def odom_callback(self, msg, robot_idx):
    self.odoms[robot_idx] = msg

  def ctrl_state_callback(self, msg, robot_idx):
    self.states[robot_idx] = msg

  def robot_clear_goals(self, robot_idx):
    return self.clear_goals_svcs[robot_idx]()
    
  def robot_add_goals(self, robot_idx, goals):
    rvals = []
    if type(goals) is not list:
      goals = list(goals)
    for goal in goals:
      rvals.append(self.add_goal_svcs[robot](goal))
    return rvals
    