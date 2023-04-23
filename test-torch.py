import torch


if torch.cuda.is_available():
    available = "GPU is available." + "\n" \
                + "Device count is " + str(torch.cuda.device_count()) + "\n" \
                + "Device name is " + torch.cuda.get_device_name(0)
else:
    available = "GPU is not available. Sorry."

print(available)