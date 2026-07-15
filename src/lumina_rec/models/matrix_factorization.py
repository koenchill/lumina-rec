import torch
import torch.nn as nn


class MatrixFactorizationModel(nn.Module):
    def __init__(self, num_users: int, num_movies: int, embedding_dim: int):
        super().__init__()

        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.movie_embedding = nn.Embedding(num_movies, embedding_dim)
        self.user_bias = nn.Embedding(num_users, 1)
        self.movie_bias = nn.Embedding(num_movies, 1)
        self.global_bias = nn.Parameter(torch.zeros(1))

    def forward(self, user_idx: torch.Tensor, movie_idx: torch.Tensor) -> torch.Tensor:
        user_vector = self.user_embedding(user_idx)
        movie_vector = self.movie_embedding(movie_idx)

        dot_product = (user_vector * movie_vector).sum(dim=1)
        user_bias = self.user_bias(user_idx).squeeze()
        movie_bias = self.movie_bias(movie_idx).squeeze()

        rating = dot_product + user_bias + movie_bias + self.global_bias
        return torch.clamp(rating, min=0.5, max=5.0)
