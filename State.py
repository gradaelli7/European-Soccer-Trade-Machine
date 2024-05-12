class State:

	def __init__(self, players, requested_positions, budget):
		self.players = players
		self.requested_positions = requested_positions
		self.budget = budget

		self.player_names = []
		for player in players:
			self.player_names.append(player['name'])

	def __hash__(self):
		return hash(tuple(self.player_names))

	def depth(self):
		return 1;

	def heuristic(self):
		heur = 0.0
		for player in self.players:
			heur -= (player['rating'] / len(self.players))
		return heur;