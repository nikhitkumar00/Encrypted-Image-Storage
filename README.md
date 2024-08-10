# Encrypted Image Storage Application

This application is a user-friendly tool for managing and viewing encrypted images. Built with Python and featuring a modern graphical interface, this tool provides secure storage for your images using AES encryption.

## Features

- **Login Screen**: Securely access the application using a paraphrase.
- **Image Handling**: Easily upload, view, and navigate through your images.
- **Encryption**: AES encryption ensures that your images are stored securely.
- **Resizable UI**: The image display adjusts to fit the window size, making it adaptable to various screen sizes.

## How It Works

The application employs AES (Advanced Encryption Standard) to secure your images. Here's a brief overview of how the paraphrase is used in the encryption and decryption process:

1. **Paraphrase Usage**:
   - When you upload an image, the application uses your paraphrase to generate an encryption key. This key is derived from the paraphrase using a key derivation function (PBKDF2HMAC) along with a random salt.
   - The generated key is then used to encrypt the image data. The image is encrypted with AES in CTR (Counter) mode, ensuring that only users with the correct paraphrase can decrypt and view the image.

2. **Impact of Paraphrase**:
   - The paraphrase directly affects the encryption key. If you enter a different paraphrase, the generated key will be different. Consequently, images encrypted with one paraphrase cannot be decrypted with a different paraphrase, rendering the images inaccessible or corrupted.
   - It is crucial to remember your paraphrase. If lost, you will not be able to decrypt and view your previously encrypted images.

## Database

- **SQLite**: The application uses an SQLite database (`database.db`) to store encrypted images and their metadata. SQLite is a lightweight, file-based database that requires no separate server installation.

## Prerequisites

- Python 3.8 or later
- Pip (Python package installer)

## Installation and Setup

1. **Clone the Repository**:
   - Use the following command to clone the repository to your local machine:
     ```bash
     git clone https://github.com/nikhitkumar00/Encrypted-Image-Storage
     ```

2. **Navigate to the Project Directory**:
   - Change to the directory where the project was cloned:
     ```bash
     cd encrypted-image-storage
     ```

3. **Run the Application**:
   - Execute the `run.bat` file to set up the environment and start the application:
     ```bash
     run.bat
     ```

4. **Using the Application**:
   - **Login**: Enter your paraphrase to access the home page.
   - **Upload Images**: Click the "Upload Images" button to add new images to the system.
   - **View Images**: Use the "Previous" and "Next" buttons to navigate through the images.

## Dependencies

The application requires the following Python packages:

- `Pillow`: For image handling.
- `cryptography`: For encrypting and decrypting images.
- `sqlite3`: For database operations.

These dependencies are listed in the `requirements.txt` file and will be installed automatically by the `run.bat` script.

## Troubleshooting

- **AttributeError**: If you encounter an error related to `numpy.typing` (e.g., `AttributeError: module 'numpy.typing' has no attribute 'NDArray'`), ensure that you have the latest version of `numpy`. Update it with:
  ```bash
  pip install --upgrade numpy
  ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you would like to contribute to this project. I appreciate all contributions, big or small. Whether you’re fixing bugs, adding new features, or improving documentation, your input helps make this project better!

## Contact

For any issues or questions, please contact [Nikhit Kumar](mailto:nikhitkumar00@gmail.com).
