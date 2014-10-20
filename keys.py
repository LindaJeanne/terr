import arena

movement = {
    55: arena.dir_nw,
    56: arena.dir_north,
    57: arena.dir_ne,
    54: arena.dir_se,
    50: arena.dir_south,
    49: arena.dir_sw,
    52: arena.dir_west}

non_turn = {
    ord('q'): arena.quit
}

turn = {
    ord('5'): arena.pass_turn
}
