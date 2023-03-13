import torch

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    x = torch.Tensor([1, 2, 3, 4])
    y = torch.Tensor([5, 6, 7, 8])
    return x + y
