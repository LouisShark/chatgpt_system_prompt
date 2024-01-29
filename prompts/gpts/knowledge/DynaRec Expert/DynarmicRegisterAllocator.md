# Register Allocation (x64 Backend)

`HostLoc`s contain values. A `HostLoc` ("host value location") is either a host CPU register or a host spill location.

Values once set cannot be changed. Values can however be moved by the register allocator between `HostLoc`s. This is
handled by the register allocator itself and code that uses the register allocator need not and should not move values
between registers.

The register allocator is based on three concepts: `Use`, `Def` and `Scratch`.

* `Use`: The use of a value.
* `Define`: The definition of a value, this is the only time when a value is set.
* `Scratch`: Allocate a register that can be freely modified as one wishes.

Note that `Use`ing a value decrements its `use_count` by one. When the `use_count` reaches zero the value is discarded and no longer exists.

The member functions on `RegAlloc` are just a combination of the above concepts.

### `Scratch`

    Xbyak::Reg64 ScratchGpr(HostLocList desired_locations = any_gpr)
    Xbyak::Xmm ScratchXmm(HostLocList desired_locations = any_xmm)

At runtime, allocate one of the registers in `desired_locations`. You are free to modify the register. The register is discarded at the end of the allocation scope.

### Pure `Use`

    Xbyak::Reg64 UseGpr(Argument& arg);
    Xbyak::Xmm UseXmm(Argument& arg);
    OpArg UseOpArg(Argument& arg);
    void Use(Argument& arg, HostLoc host_loc);

At runtime, the value corresponding to `arg` will be placed a register. The actual register is determined by
which one of the above functions is called. `UseGpr` places it in an unused GPR, `UseXmm` places it
in an unused XMM register, `UseOpArg` might be in a register or might be a memory location, and `Use` allows
you to specify a specific register (GPR or XMM) to use.

This register **must not** have it's value changed.

### `UseScratch`

    Xbyak::Reg64 UseScratchGpr(Argument& arg);
    Xbyak::Xmm UseScratchXmm(Argument& arg);
    void UseScratch(Argument& arg, HostLoc host_loc);

At runtime, the value corresponding to `arg` will be placed a register. The actual register is determined by
which one of the above functions is called. `UseScratchGpr` places it in an unused GPR, `UseScratchXmm` places it
in an unused XMM register, and `UseScratch` allows you to specify a specific register (GPR or XMM) to use.

The return value is the register allocated to you.

You are free to modify the value in the register. The register is discarded at the end of the allocation scope.

### `Define` as register

A `Define` is the defintion of a value. This is the only time when a value may be set.

    void DefineValue(IR::Inst* inst, const Xbyak::Reg& reg);

By calling `DefineValue`, you are stating that you wish to define the value for `inst`, and you have written the
value to the specified register `reg`.

### `Define`ing as an alias of a different value

Adding a `Define` to an existing value.

    void DefineValue(IR::Inst* inst, Argument& arg);

You are declaring that the value for `inst` is the same as the value for `arg`. No host machine instructions are
emitted.

## When to use each?

* Prefer `Use` to `UseScratch` where possible.
* Prefer the `OpArg` variants where possible.
* Prefer to **not** use the specific `HostLoc` variants where possible.
