def calc_angular_coeffs(self) -> Matrix_ac:
    sep = self.separator
    from_output_side = []
    for output_side in range(sep.SIDES):
        from_emitter = []

        def calc_for_each_collector(side: int, center: Center) -> Sequence[float]:
            if side == output_side:
                # cells on the same side have angular coeffs equal to 0
                return [0] * sep.find_num_cells(side)
            return [calc_elementary_ac(center, collector, sep.normals[output_side], sep.normals[side],
                                       sep.step_size) for collector in sep[side]]

        for emitter in sep._breaks[output_side]:
            to_input_side = [calc_for_each_collector(input_side, emitter) for input_side in range(sep.SIDES)]
            from_emitter.append(to_input_side)
        from_output_side.append(from_emitter)
    return from_output_side


def convert(self, arr: Matrix_ac | Sle) -> Sle:
    if type(arr) is Sle:
        return arr
    # begin with arr[first][second][third][fourth]
    max_len, total_num = self.separator.find_max_num(), len(self.separator)
    sides = self.separator.SIDES
    buffer = [[flatten(arr[i][j]) if j < len(arr[i]) else [0] * total_num for j in range(max_len)]
              for i in range(sides)]  # arr[first][new_second][third + fourth]
    buffer = np.transpose(np.array(buffer))  # arr[third + fourth][new_second][first]
    res = []
    for i in range(total_num):
        internal_arr = np.transpose(buffer[i])  # arr[first][new_second]
        internal_arr = [internal_arr[j][:self.separator.find_num_cells(j)] for j in range(sides)]
        # arr[first][second]
        internal_arr = flatten(internal_arr)  # arr[first + second]
        res.append(internal_arr)
    return np.transpose(np.array(res))  # arr[first + second][third + fourth]
