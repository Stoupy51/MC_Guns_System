
Prompt I use with GitHub Copilot with Claude Opus to efficiently work.

```
Hello!

In my project of Minecraft Guns System, I have a few TODO in the #file:README.md I want to implement.

I want you to implement the following:

TODO: Write here


But wait, just before doing so, make sure you understand everything in the project:
- src folder will generate files using StewBeet & Beet
- assets folder contains assets
- build folder is the result of the build, never modify it
- If you need to understand minecraft vanilla bheavior, the decompiled source code is in "minecraft_source_code" folder
- based_of folder is the old code (1.19, we are in 1.21.11 / 26.1 now) : we keep it because it can always come handy if we are missing a feature.

To build the project, type `stewbeet` and verify output in build.

For each task to do, type `rm done_with_current_task_call_review_agent` command in terminal, a Review Agent will check on it and tell you if the task is good and you can continue on!
ALWAYS run this command when you're finished!
```
