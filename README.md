# tinyblog2
- See the original tinyblog: https://github.com/petabyt/tinyblog
- Personal fork of this: https://code.theres.life/p/blog/

After some PHP + Google indexing issues, I've decided to rewrite  
Tinyblog in Python.

This is meant to be a drop in upgrade for the old tinyblog, keeping  
compatibility with everything.  
If you are new to this, use `minimal.py`, which deletes all of the  
stuff keeping compatibility.  

The main change is the post URL. Instead of `?post=50`, posts are  
loaded in by a title, like:  
https://petabyt.dev/blog/tiny-embedded-module-system-spec  
This fixes several search engine indexing issues, which tend to  
index the same post at both "index.php?post=" and "/?post=".  

The file format is the same, with `posts/` containing numbered files  
starting from `1`. Each file contains some metadata:
```
The Title
Feb 1 2021
```
First line is title, second line is date. The URL is generated from  
the title.

If you want to delete a post, make it start with `:skip`.
If you want a custom title, write it in the beginning starting with a `:`.  

```
:skip
not shown...
```

```
:title
The Title
Feb 1 2021
Hello test
```
