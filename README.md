# Stackbuilder

Stackbuilder is a tool to build stacks of software from multiple sources.

## Why?

If you've ever built an application stack, you'll know that there are all sorts of ways to get the pieces on a box, and lots of ways you can link them together.

If you're really lucky you have up to date packages from your distribution and can just 'yum update', or 'apt-get update', and everthing is magically there, all upgraded to the latest version, with all the latest patches, and it all just works together tra la la.

For the rest of us there's Stackmaker, a framework that allows you to specify what your components are, where they come from, and how to build them to make a complete working stack, and reproduce/ rebuild it on demand when a component needs updating or you need something almost like it, but slightly different.