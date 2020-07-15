import argparse
from story import Story

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run TinyTines Story')
    parser.add_argument('story_file_path', help='TinyTines story json path')
    args = parser.parse_args()

    story_file_path = args.story_file_path
    # story_file_path = '../resources/tiny-tines-sunset.json'
    # print("Story File Path::" + story_file_path)

    story = Story(story_file_path)
    story.run()