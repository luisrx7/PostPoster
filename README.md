# PostPoster


>🚧 Under Development 🚧
>This tool is currently under active development. The features and usage described in this README represent the intended functionality. At present, PostPoster can only create posts and stories on Facebook. Support for additional platforms and features is forthcoming.

## Overview

**PostPoster** is a lightweight and intuitive tool designed to streamline the process of posting content across multiple social media platforms. Whether you're a small business owner or a social media manager, PostPoster empowers you to manage your social media presence efficiently without the need for complex tools or external help.

By using a declarative approach, PostPoster allows you to define the content and schedule of your posts in a simple YAML file. This tool automates the process, ensuring your posts are published on the specified platforms at the right time, reducing the repetitive and time-consuming nature of manual scheduling.

### Why PostPoster?

The project was conceived as a solution to the cumbersome and repetitive nature of tools like the Meta Business Suite scheduler. PostPoster is designed to save time and simplify the posting process, enabling users to focus on creating quality content instead of navigating complex interfaces.

## Features

- **Multi-Platform Posting:** Publish content simultaneously on Facebook and Instagram.
- **Scheduling:** Schedule your posts to be published at a specific date and time.
- **Content Customization:** Define descriptions, hashtags, and images for each post.
- **Content Types:** Support for various content formats, including posts, stories, and videos.
- **Simple Configuration:** All post details are specified in a straightforward YAML file.

## Usage

To schedule a post, define the necessary fields in the `posts.yaml` file as shown below:

```yaml
post:
  - type: "post" # post, story, video
    description: "This is a description"
    images: ["path/to/image1", "path/to/image2", "path/to/directory"] # directory/files with images 
    hashtags: ["#hashtag1", "#hashtag2"]
    date: "2021-10-10 10:00:00"
    platform: ["facebook", "instagram"]

  - type: "post" # post, story, video
    description: "This is a description of second post"
    images: ["path/to/image1", "path/to/image2", "path/to/directory"] # directory/files with images 
    hashtags: ["#hashtag1", "#hashtag2"]
    date: "2021-10-10 12:00:00"
    platform: ["facebook", "instagram"]

  - type: "story" # post, story, video
    description: "story example" # story does not support description or hashtags
    videos: ["path/to/video1", "path/to/video2", "path/to/directory"] # directory/files with videos # 1 story per video
    date: "2021-10-10 11:00:00"
    platform: ["facebook", "instagram"]
```

### Key Notes:

- **Content Types:** Specify whether the content is a `post`, `story`, or `video`.
- **Images & Videos:** Provide paths to images or videos. Directories can also be specified if multiple files are involved.
- **Platform:** List the platforms where the content should be published (currently supports Facebook and Instagram).
- **Scheduling:** Use the `date` field to set the exact time for the post to go live.

## Getting Started

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/luisrx7/PostPoster.git
   ```

2. **Install Dependencies:**  
   Follow the instructions in the `requirements.txt` file or set up the environment as specified.

3. **Configure Posts:**  
   Edit the `posts.yaml` file to define your posts.

4. **Run the Scheduler:**  
   Execute the posting script to schedule your content according to the specified configurations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any improvements or feature requests.

---

This improved README provides a clearer structure, adds more detail to the overview, and ensures consistency throughout. It also includes a "Getting Started" section to help new users quickly set up and use the tool.