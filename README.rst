A utility used to collect timing (profiling) data about functions.

For each function annotated, all of that function's runtimes will be
tracked.  When the process terminates, all collected metrics are
summarized.

Example:

    import sys
    from timefn import timefn
    
    @timefn
    def addem(a, b):
        return a + b
    
    @timefn
    def subem(a, b):
        return a - b

    def main(argv):
        for i in range(3)
            print(addem(i, i + 1))

        for i in range(3):
            print(subem(i, i + 1))

    return 0

    if __name__ == '__main__':
        sys.exit( main(sys.argv) )
    
 This would output:

    localhost:~/src$ python ~/test.py
    1
    3
    5
    -1
    -1
    -1
    
    Report for: addem
        times called:         3
        min value:     0.000001 [0]
        max value:     0.000001 [0]
        avg value:     0.000001
    
    Report for: subem
        times called:         3
        min value:     0.000000 [2]
        max value:     0.000001 [0]
        avg value:     0.000001
