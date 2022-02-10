# tinyblog2
- See the original tinyblog: https://github.com/petabyt/tinyblog
- Personal fork of this: https://code.theres.life/p/blog/

After some PHP + Google indexing issues, I've decided to rewrite  
Tinyblog in Python.

This is meant to be a drop in upgrade for the old tinyblog, keeping  
compatibility with everything.  
The main change is the post URL. Instead of `?post=50`, posts are  
loaded in by a title, like:  
https://petabyt.dev/blog/tiny-embedded-module-system-spec  

This fixes several search engine indexing issues, which tend to  
index the same post at both "index.php?post=" and "/?post=".  

I didn't keep line count in mind this time, although I kept it  
fairly small. I could have done better if it weren't for my picky  
markdown parsing.

Comes with a custom markdown parser and RSS.xml output.
