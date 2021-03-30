class Coordinate():
    """Coordinate validates coordinate data and converts coordinate systems.

    Chromosome, start, stop, reference and variant values are validated to
    a one-based or zero-based coordinate system. Following validation the
    coordinate data is converted to one-based or zero-based coordinate systems
    using the to_base() function.

    Attributes:
        chromosome (str): Chromosome name.
        start (int): Starting coordinate.
        stop (int): Ending coordinate.
        ref (str): Genome reference base.
        var (str): Variant base.
        zero_one_based (1 or 0): 1 if coordinate is one-based, 0 if zero-based.
        is_valid (bool): True if coordinate is valid one-based or zero-based
            coordinate system, False otherwise.
        is_insertion (bool): True is coordinate is an insertion.
        is_snv (bool): True if coordinate is single nucleotide variant.
    """

    def __init__(self, chromosome, start, stop, ref, var):
        """Initialize and validate coordinate.

        Args:
            chromosome (str): Chromosome name.
            start (int): Starting coordinate.
            stop (int): Ending coordinate.
            ref (str): Genome reference base.
            var (str): Variant base.
        """
        self._valid_coord = True
        self._set_coordinate(chromosome, start, stop, ref, var)

    def _set_coordinate(self, chromosome, start, stop, ref, var):
        """"""
        self.chromosome = chromosome
        self.start = start
        self.stop = stop
        self.ref = ref
        self.var = var
        self._determine_mutation_type()
        self._determine_coordinate_system()

    def _determine_mutation_type(self):
        """Determines the mutation type from start, stop, ref, var"""

        if self.ref in ['-', '.', '0']:
            self.mutation_type = 'ins'
        elif self.var in ['-', '.', '0']:
            self.mutation_type = 'del'
        elif len(self.ref) == 1 and len(self.var) == 1:
            self.mutation_type = 'snv'
        elif len(self.ref) == len(self.var) and len(self.ref) > 1:
            self.mutation_type = 'sub'
        else:
            raise ValueError('The coordinate inputs do not resolve to a valid '
                             'variant type (snv, ins, del, sub).')

    def _determine_coordinate_system(self):
        """Determines the coordinate system using the coordinates and inferred
        mutation type."""
        if not self._valid_coord:
            pass
        if self.mutation_type is 'snv':
            if self.start+1 == self.stop:
                self.coordinate_system = 0
            elif self.start == self.stop:
                self.coordinate_system = 1
            else:
                raise ValueError('The reference and variant fields indicate a '
                                 'single nucleotide variant, however the '
                                 'coordinates (start and stop) are not valid '
                                 'for this mutation type')
        elif self.mutation_type is 'ins':
            if self.start == self.stop:
                self.coordinate_system = 0
            elif self.start == self.stop-1:
                self.coordinate_system = 1
            else:
                raise ValueError('The reference and variant fields indicate '
                                 'an insertion variant, however the '
                                 'coordinates (start and stop) are not valid '
                                 'for this mutation type.')
        elif self.mutation_type in ['del', 'sub']:
            if self.start + len(self.ref) == self.stop:
                self.coordinate_system = 0
            elif self.stop - self.start == len(self.ref)-1:
                self.coordinate_system = 1
            else:
                raise ValueError('The reference and variant fields indicate '
                                 'an deletion or substitution variant, '
                                 'however the coordinates (start and stop) '
                                 'are not valid for these mutation types.')

    def to_zero_based(self):
        """Converts coordinate to zero-based and returns a tab-delimited string.

        Returns:
            Tab-delimited string of coordinates in zero-based coordinate
                system. Values are positionally formatted as chromosome, start,
                stop, reference, variant.
        """
        return ''

    def to_one_based(self):
        """Converts coordinate to one-based and returns a tab-delimited string.

        Returns:
            Tab-delimited string of coordinates in one-based coordinate system.
                Values are positionally formatted as chromosome, start, stop,
                reference, variant.
        """
        return ''

    def is_valid(self):
        return self._valid_coord
