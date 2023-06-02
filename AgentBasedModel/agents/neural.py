import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


# Define the DQN class
class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# Define the DQN Agent
class DQNAgent:
    def __init__(self, input_size, output_size, hidden_size, learning_rate, discount_factor, exploration_rate):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Create the DQN and target network
        self.dqn = DQN(input_size, hidden_size, output_size).to(self.device)
        self.target_dqn = DQN(input_size, hidden_size, output_size).to(self.device)
        self.target_dqn.load_state_dict(self.dqn.state_dict())
        self.target_dqn.eval()

        self.optimizer = optim.Adam(self.dqn.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()

        self.replay_memory = []  # Experience replay memory

    def act(self, state):
        with torch.no_grad():
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
            q_values = self.dqn(state_tensor)
            action = torch.argmax(q_values).item()
            return action

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.exploration_rate:
            # Explore: select a random action
            action = np.random.choice(self.output_size)
        else:
            # Exploit: select the action with the highest Q-value
            action = self.act(state)
        return action

    def update_replay_memory(self, state, action, reward, next_state, done):
        self.replay_memory.append((state, action, reward, next_state, done))

    def update_dqn(self, batch_size):
        if len(self.replay_memory) < batch_size:
            return

        # Sample a batch of experiences from the replay memory
        batch = np.random.choice(len(self.replay_memory), batch_size, replace=False)
        states, actions, rewards, next_states, dones = zip(*[self.replay_memory[i] for i in batch])

        states_tensor = torch.tensor(states, dtype=torch.float32).to(self.device)
        actions_tensor = torch.tensor(actions, dtype=torch.long).unsqueeze(1).to(self.device)
        rewards_tensor = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1).to(self.device)
        next_states_tensor = torch.tensor(next_states, dtype=torch.float32).to(self.device)
        dones_tensor = torch.tensor(dones, dtype=torch.float32).unsqueeze(1).to(self.device)

        # Compute target Q-values using the target network
        with torch.no_grad():
            target_q_values = rewards_tensor + self.discount_factor * (1 - dones_tensor) * torch.max(self.target_dqn(next_states_tensor), dim=1, keepdim=True)[0]

        # Compute current Q-values using the DQN
        q_values = self.dqn(states_tensor).gather(1, actions_tensor)

        # Update the DQN network
        loss = self.criterion(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_network(self):
        self.target_dqn.load_state_dict(self.dqn.state_dict())

    def save_model(self, file_path):
        torch.save({
            'model_state_dict': self.dqn.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, file_path)

    def load_model(self, file_path):
        checkpoint = torch.load(file_path)
        self.dqn.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.dqn.eval()



    # Example usage:


