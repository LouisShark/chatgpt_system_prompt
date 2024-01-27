# Encrypting Strings at Compile Time

> Thank you to [SpecterOps](https://specterops.io/) for supporting this research and to [Duane](https://twitter.com/subat0mik) and [Matt](https://twitter.com/matterpreter) for proofreading and editing!
> Crossposted on the [SpecterOps Blog](https://posts.specterops.io/encrypting-strings-at-compile-time-4141dafe5b41).

TLDR: _You may use [this header file](https://gist.github.com/EvanMcBroom/ad683e394f84b623da63c2b95f6fb547) for reliable compile time string encryption without needing any additional dependencies._

Programmers of DRM software, security products, or other sensitive code bases are commonly required to minimize the amount of human readable strings in binary output files. The goal of the minimization is to hinder others from reverse engineering their proprietary technology.

Common approaches that are taken to meet this requirement often add an additional maintenance burden to the developer and are prone to error. These approaches will be presented along with their drawbacks. An alternative solution will also be presented which targets the following goals:
- A minimalistic implementation to ease integration into projects
- A simple usage design to avoid programmer error
- Builtin randomization to hinder automated string recovery

## Common Approaches

Separate utilities are commonly built to precompute obfuscated strings for use in source code. Such tools will generate a header file or other output that must be manually added to and referenced in projects. The use of these tools may be automated with a toolchain but they will not integrate well with IDEs and they are tedious to maintain as more strings are added. They also tend to obfuscate strings in a uniform way that can be easily identified and reversed in an automated fashion.

In a similar manner, utilities are also commonly built to precompute string hashes for use in comparisons. One of the earliest examples of this is documented in "Win32 Assembly Components."<sup>1</sup> These tools are also tedious to maintain as more strings are added but they can now be completely eliminated by hashing strings at compile time [as described in a previous post](https://gist.github.com/EvanMcBroom/2a9bed888c2755153a9616aa7ae1f79a).

Lastly, some development teams attempt to remove the use of strings entirely. Needless to say this is an impossible standard to maintain for any large or long lasting project with any amount of developer turnover.

## An Alternative Solution

Modern C++ features may be used to encrypt strings at compile time which can greatly reduce the maintenance overhead for developers. There are several libraries that claim to support this use case. Unfortunately, they rarely work in practice. The few that do require [BOOST](https://www.boost.org/) libraries which may not be an option due to development constraints.<sup>2</sup> So we will build our own!

We will first make a basic function for compile time string encryption which we can later improve upon. The below `crypt` function will convert a string literal into an encrypted blob and the `make_string` macro wraps `crypt` to ensure that it is used correctly to be evaluated at compile time.

```cpp
template<typename T, size_t N>
struct encrypted {
    T data[N];
};

template<size_t N>
constexpr auto crypt(const char(&input)[N]) {
    encrypted<char> blob{};
    for (uint32_t index{ 0 }; index < N; index++) {
        blob.data[index] = input[index] ^ 'A';
    }
    return blob;
}

#define make_string(STRING) ([&] {            \
    constexpr auto _{ crypt(STRING) };        \
    return std::string{ crypt(_.data).data }; \
}())
```

The `make_string` macro will also expand to a single lambda expression which can be used for any variable assignment and argument passing operation.

```cpp
void main() {
    std::string string1{ make_string("String 1") };
    std::string string2 = make_string("String 2");
    func(make_string("String 3"));
}
```

## Improving the Solution

The previous solution would be easy to integrate and use in projects but it would also be easy for a reverse engineer to undo. It is essentially a XOR cipher with a static key. Once the key is identified the entire program can be XORed with it and then the original strings can be recovered using the humble `strings` utility.

Replacing the static key with a random bit stream would prevent this issue. We will now make a set of functions for generating such a stream at compile time. We will use Park-Miller's "Multiplicative Linear Congruential Generator" due to its simplicity to implement.<sup>3</sup>

```cpp
constexpr uint32_t modulus() {
    return 0x7fffffff;
}

constexpr uint32_t prng(const uint32_t input) {
    return (input * 48271) % modulus();
}
```

We will also need a pseudorandom value to use as the initial input to `prng`. Admittedly, it is not easy to generate such a value at compile time but it can be accomplished using standard predefined macros such as `__FILE__` and `__LINE__`. The below `seed` function can take these macros as input and reduce them to a single pseudorandom value to use with `prng`.

> Note: These macros are defined by the ANSI C standard and are supported by all compilers. If you use a non-standard macro for entropy your mileage may vary. 

```cpp
template<size_t N>
constexpr uint32_t seed(const char(&entropy)[N], const uint32_t iv = 0) {
    auto value{ iv };
    for (size_t i{ 0 }; i < N; i++) {
        // Xor 1st byte of seed with input byte
        value = (value & ((~0) << 8)) | ((value & 0xFF) ^ entropy[i]);
        // Rotate left 1 byte
        value = value << 8 | value >> ((sizeof(value) * 8) - 8);
    }
    // The seed is required to be less than the modulus and odd
    while (value > modulus()) value = value >> 1;
    return value << 1 | 1;
}
```

The last thing that is required is to update our original `crypt` and `make_string` functions to use our random bit stream generator.

```cpp
template<typename T, size_t N>
struct encrypted {
    int seed;
    T data[N];
};

template<size_t N>
constexpr auto crypt(const char(&input)[N], const uint32_t seed = 0) {
    encrypted<char, N> blob{};
    blob.seed = seed;
    for (uint32_t index{ 0 }, stream{ seed }; index < N; index++) {
        blob.data[index] = input[index] ^ stream;
        stream = prng(stream);
    }
    return blob;
}

#define make_string(STRING) ([&] {                               \
    constexpr auto _{ crypt(STRING, seed(__FILE__, __LINE__)) }; \
    return std::string{ crypt(_.data, _.seed).data };            \
}())
```

> Note: If you are using Visual Studio, you will need to disable the "Edit and Continue" feature; otherwise, [the `__LINE__` macro will not need be usable in a constant expression](https://developercommunity.visualstudio.com/t/-line-cannot-be-used-as-an-argument-for-constexpr/195665#T-N197532).

## Incident Response

If you are investigating a potentially malicious executable, it may also contain strings encrypted in such a manner. The provided code will protect strings against any cursory inspection, but they may all be recovered using [FLARE's Obfuscated String Solver](https://github.com/mandiant/flare-floss) (FLOSS).

Additional small improvements may be made to prevent automated string recovery using FLOSS as well. One example would be to include an exception based control flow to the decryption routine. In the interest of incident responders though, these improvements will not be presented and are left as an exercise to the reader.

## Conclusion

We now have a solution for encrypting strings at compile time that meets all of our original goals and will work with any mainstream compiler. The full source for which can be found [here](https://gist.github.com/EvanMcBroom/ad683e394f84b623da63c2b95f6fb547). Enjoy! :smile:

If you enjoyed reading this work, you may enjoy some of my older posts as well. The first covers compile time hashing functions and the second gives a more user friendly alternative to the programming idiom for declaring strings in position independent code.

- [Switch Statements with Full Strings](https://gist.github.com/EvanMcBroom/2a9bed888c2755153a9616aa7ae1f79a)
- PIC and String Literals [Part 1](https://gist.github.com/EvanMcBroom/f5b1bc53977865773802d795ade67273) and [Part 2](https://gist.github.com/EvanMcBroom/d7f6a8fe3b4d8f511b132518b9cf80d7)

## References

1. The Last Stage of Delirium Research Group. _Win32 Assembly Components_, 2002.
`http://www.lsd-pl.net/documents/winasm-1.0.1.pdf`
2. Sebastien Andrivet. _C++11 Metaprogramming Applied to Software Obfuscation_, 2014.
`https://www.blackhat.com/docs/eu-14/materials/eu-14-Andrivet-C-plus-plus11-Metaprogramming-Applied-To-software-Obfuscation-wp.pdf`
3. Stephen Park and Keith Miller. _Random Number Generators_, 1988.
`https://www.firstpr.com.au/dsp/rand31/p1192-park.pdf`