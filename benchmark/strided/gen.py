import argparse
import subprocess

def make_parser():
    parser = argparse.ArgumentParser(
        description='Generate strided test program')
    #parser.add_argument('-C', action='store_true',
                        #help='compile generated program')
    parser.add_argument('-n', default=16, type=int,
                        help='size of array')
    parser.add_argument('-s', default=2, type=int,
                        help='access stride')
    return parser

def generate_code(opts):
    # Computer correct reduction value.
    red = 0
    for v in range(0, opts.n, opts.s):
        red += v

    code = f'''
#include <assert.h>
#include <immintrin.h>

#define ARRSIZE {opts.n}
#define STRIDE {opts.s}

int main(int argc, char *argv[]) {{
  // Populate array.
  int arr[ARRSIZE];
  for (int i = 0; i < ARRSIZE; i++)
    arr[i] = i;

  // Flush cache.
  for (int i = 0; i < ARRSIZE; i += 8)
    _mm_clflush(&arr[i]);

  // Perform strided reduction.
  int red = 0;
  for (int i = 0; i < ARRSIZE; i += STRIDE)
    red += arr[i];

  assert(red == {red});

  return EXIT_SUCCESS;
}}
'''

    return code.strip()

def fname(opts):
    return f'strided_{opts.n}_{opts.s}'

if __name__ == '__main__':
    parser = make_parser()
    opts = parser.parse_args()

    cpp_fname = fname(opts) + '.cpp'
    with open(cpp_fname, 'w') as ofs:
        ofs.write(generate_code(opts))
