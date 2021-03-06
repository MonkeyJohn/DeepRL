#######################################################################
# Copyright (C) 2017 Shangtong Zhang(zhangshangtong.cpp@gmail.com)    #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

from .base_network import *

# Network for CartPole with value based methods
class FCNet(nn.Module, VanillaNet):
    def __init__(self, dims, gpu=True):
        super(FCNet, self).__init__()
        self.fc1 = nn.Linear(dims[0], dims[1])
        self.fc2 = nn.Linear(dims[1], dims[2])
        self.fc3 = nn.Linear(dims[2], dims[3])
        BasicNet.__init__(self, gpu)

    def forward(self, x):
        x = self.to_torch_variable(x)
        x = x.view(x.size(0), -1)
        y = F.relu(self.fc1(x))
        y = F.relu(self.fc2(y))
        y = self.fc3(y)
        return y

# Network for CartPole with dueling architecture
class DuelingFCNet(nn.Module, DuelingNet):
    def __init__(self, dims, gpu=True):
        super(DuelingFCNet, self).__init__()
        self.fc1 = nn.Linear(dims[0], dims[1])
        self.fc2 = nn.Linear(dims[1], dims[2])
        self.fc_value = nn.Linear(dims[2], 1)
        self.fc_advantage = nn.Linear(dims[2], dims[3])
        BasicNet.__init__(self, gpu)

    def forward(self, x):
        x = self.to_torch_variable(x)
        x = x.view(x.size(0), -1)
        y = F.relu(self.fc1(x))
        phi = F.relu(self.fc2(y))
        return phi

# Network for CartPole with actor critic
class ActorCriticFCNet(nn.Module, ActorCriticNet):
    def __init__(self, state_dim, action_dim):
        super(ActorCriticFCNet, self).__init__()
        hidden_size1 = 64
        hidden_size2 = 64
        self.fc1 = nn.Linear(state_dim, hidden_size1)
        self.fc2 = nn.Linear(hidden_size1, hidden_size2)
        self.fc_actor = nn.Linear(hidden_size2, action_dim)
        self.fc_critic = nn.Linear(hidden_size2, 1)
        BasicNet.__init__(self, False)

    def forward(self, x, update_LSTM=True):
        x = self.to_torch_variable(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        phi = self.fc2(x)
        return phi
