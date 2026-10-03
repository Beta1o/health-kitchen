import sys
f=sys.argv[1];s=open(f).read().replace("]))\n)","])}))")
s=s.replace("]))\nsave","])}))\nsave")
open(f,'w').write(s)
