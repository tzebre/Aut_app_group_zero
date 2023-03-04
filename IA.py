# architecture : encoder +algo génetique + decoder
# - Je pense que le système encoder decoder à besoin d'être pretrain, et ensuite on y ajoute au milieu l'algo génetique: encoder+decoder pretrain saura retrouver une image, la reconstituer
# - Une fois qu'on ajoute l'lago génetique cela reconstruira une image mais modifiée puisqu'on aura changer la matrice en sortie de l'encoder
# Training encoder-decoder

# import library

import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.utils.data import Dataset
# from torch import optim
# from torch.autograd import Variable
# from torch.nn import functional as F
from torchvision import transforms
from PIL import Image
import os
from sklearn.model_selection import train_test_split

## Ouverture des images et création des dataloaders
contenu = os.listdir('image')
# print(contenu)
convert_tensor = transforms.ToTensor()
dataset = []
data_dir = "image"

for i in range(len(contenu)):
    img_path = os.path.join(data_dir, contenu[i])
    img = Image.open(img_path)
    tensor = convert_tensor(img)
    dataset.append(tensor)

# print(dataset)

X_train, X_test = train_test_split(dataset, test_size=0.2, random_state=0)
X_train, X_val = train_test_split(X_train, test_size=0.25, random_state=0)

batch_size = 1

train_loader = torch.utils.data.DataLoader(X_train, batch_size=batch_size)
valid_loader = torch.utils.data.DataLoader(X_val, batch_size=batch_size)
test_loader = torch.utils.data.DataLoader(X_test, batch_size=batch_size, shuffle=True)


class Encoder(torch.nn.Module):
    def __init__(self, encoded_dim):
        super(Encoder, self).__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Conv2d(1, 64, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.MaxPool2d(2, padding=1),
            torch.nn.Dropout(0.2),
            torch.nn.Conv2d(64, 32, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.MaxPool2d(2, padding=1),
            torch.nn.Dropout(0.2),
            torch.nn.Conv2d(32, 16, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.MaxPool2d(2, padding=1),
            torch.nn.Dropout(0.2),
            torch.nn.Conv2d(16, 8, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.MaxPool2d(2, padding=1),
            torch.nn.Dropout(0.2))

        self.flatten = torch.nn.Flatten(start_dim=1)

        self.encoder_lin = torch.nn.Sequential(
            torch.nn.Linear(3 * 3 * 64, 128),
            torch.nn.ReLU(True),
            nn.Linear(128, encoded_dim))

    def forward(self, x):
        x = self.encoder(x)
        x = self.flatten(x)
        x = self.encoder_lin(x)
        return x


class Decoder(torch.nn.Module):
    def __init__(self, encoded_dim):
        super(Decoder, self).__init__()
        self.decoder = torch.nn.Sequential(
            nn.Linear(encoded_dim, 128),
            nn.ReLU(True),
            nn.Linear(128, 4 * 4 * 8),
            nn.ReLU(True))

        self.decoder_next = torch.nn.Sequential(
            torch.nn.Conv2d(1, 8, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.UpsamplingNearest2d(size=(2, 2)),
            torch.nn.Dropout(0.2),
            torch.nn.Conv2d(8, 16, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.UpsamplingNearest2d(size=(2, 2)),
            torch.nn.Dropout(0.2),
            torch.nn.Conv2d(16, 32, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.UpsamplingNearest2d(size=(2, 2)),
            torch.nn.Dropout(0.2),
            torch.nn.Conv2d(32, 64, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.ReLU(True),
            torch.nn.UpsamplingNearest2d(size=(2, 2)),
            torch.nn.Conv2d(64, 1, kernel_size=(3, 3), stride=1, padding=1),
            torch.nn.Sigmoid())

    def forward(self, x):
        x = self.decoder(x)
        torch.reshape(x, (4, 4, 8))
        x = self.decoder_next(x)
        return x


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
loss_fn = torch.nn.MSELoss()
lr = 0.001
dim = 10
torch.manual_seed(0)

encoder = Encoder(encoded_dim=dim)
decoder = Decoder(encoded_dim=dim)
params_to_optimize = [
    {'params': encoder.parameters()},
    {'params': decoder.parameters()}
]

optim = torch.optim.Adam(params_to_optimize, lr=lr, weight_decay=1e-05)
encoder.to(device)
decoder.to(device)


def train_epoch(encoder, decoder, device, dataloader, loss_fn, optimizer):
    # Set train mode for both the encoder and the decoder
    encoder.train()
    decoder.train()
    train_loss = []
    # Iterate the dataloader (we do not need the label values, this is unsupervised learning)
    for image_batch, in dataloader:  # with "_" we just ignore the labels (the second element of the dataloader tuple)
        # Move tensor to the proper device
        image_batch = image_batch.to(device)
        # Encode data
        encoded_data = encoder(image_batch)
        # Decode data
        decoded_data = decoder(encoded_data)
        # Evaluate loss
        loss = loss_fn(decoded_data, image_batch)
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # Print batch loss
        print('\t partial train loss (single batch): %f' % (loss.data))
        train_loss.append(loss.detach().cpu().numpy())

    return np.mean(train_loss)


def test_epoch(encoder, decoder, device, dataloader, loss_fn):
    # Set evaluation mode for encoder and decoder
    encoder.eval()
    decoder.eval()
    with torch.no_grad():  # No need to track the gradients
        # Define the lists to store the outputs for each batch
        conc_out = []
        conc_label = []
        for image_batch, _ in dataloader:
            # Move tensor to the proper device
            image_batch = image_batch.to(device)
            # Encode data
            encoded_data = encoder(image_batch)
            # Decode data
            decoded_data = decoder(encoded_data)
            # Append the network output and the original image to the lists
            conc_out.append(decoded_data.cpu())
            conc_label.append(image_batch.cpu())
        # Create a single tensor with all the values in the lists
        conc_out = torch.cat(conc_out)
        conc_label = torch.cat(conc_label)
        # Evaluate global loss
        val_loss = loss_fn(conc_out, conc_label)
    return val_loss.data


def plot_ae_outputs(encoder, decoder, n=10):
    plt.figure(figsize=(16, 4.5))
    targets = X_test.targets.numpy()
    t_idx = {i: np.where(targets == i)[0][0] for i in range(n)}
    for i in range(n):
        ax = plt.subplot(2, n, i + 1)
        img = X_test[t_idx[i]][0].unsqueeze(0).to(device)
        encoder.eval()
        decoder.eval()
        with torch.no_grad():
            rec_img = decoder(encoder(img))
        plt.imshow(img.cpu().squeeze().numpy(), cmap='gist_gray')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        if i == n // 2:
            ax.set_title('Original images')
        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(rec_img.cpu().squeeze().numpy(), cmap='gist_gray')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        if i == n // 2:
            ax.set_title('Reconstructed images')
    plt.show()


num_epochs = 30
diz_loss = {'train_loss': [], 'val_loss': []}
for epoch in range(num_epochs):
    train_loss = train_epoch(encoder, decoder, device,
                             train_loader, loss_fn, optim)
    val_loss = test_epoch(encoder, decoder, device, test_loader, loss_fn)
    print('\n EPOCH {}/{} \t train loss {} \t val loss {}'.format(epoch + 1, num_epochs, train_loss, val_loss))
    diz_loss['train_loss'].append(train_loss)
    diz_loss['val_loss'].append(val_loss)
    plot_ae_outputs(encoder, decoder, n=10)
