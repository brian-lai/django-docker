def parse_genomic_coordinate(genomic_coordinate_long):
    '''Performs 28-bit shift for extracting locus and position.

    249 million is the largest position on a single chromosome in the human genome.
    '''
    position_mask = 0xFFFFFFFL
    # Make sure the long is within the bounds of a valid chrom/position
    if genomic_coordinate_long < 268435456 or genomic_coordinate_long > 14227079167:
        raise ValueError('Invalid human genomic coordinate')

    # Parse out information
    position = genomic_coordinate_long & position_mask
    chromosome = genomic_coordinate_long >> 28

    return chromosome, position


class GenomicCoordinate(object):
    '''DB assitant for efficiently decoding and querying for genomic coordinates.
    '''
    __slots__ = ('chromosome', 'position')

    # Which chromosome is the found on?
    CHROMOSOME_CHOICES = (
        (1, '1'), (2, '2'), (3, '3'), (4, '4'),
        (5, '5'), (6, '6'), (7, '7'), (8, '8'),
        (9, '9'), (10, '10'), (11, '11'), (12, '12'),
        (13, '13'), (14, '14'), (15, '15'), (16, '16'),
        (17, '17'), (18, '18'), (19, '19'), (20, '20'),
        (21, '21'), (22, '22'), (23, 'M'),
        (24, 'X'), (25, 'Y'),
    )

    # Transforms for forwards and reverse lookups done at 'compile' time.
    # Where forwards is going from an internal representaton (numeric)
    # to a human readable format, and reverse obviously back to machine land.
    _forward_chromosomes = {
        chrom[0]: chrom[1]
        for chrom in CHROMOSOME_CHOICES
    }
    _reverse_chromosomes = {
        chrom[1]: chrom[0]
        for chrom in CHROMOSOME_CHOICES
    }

    def __init__(self, chromosome=None, position=None, locus=None):
        '''Allows either separate or combinded coordinates to be provided.
        '''
        if locus is not None:
            self.chromosome, self.position = locus.split(':')
            self.position = self.position
        elif position is not None:
            self.position = position
            # If a chromosome is provided, the position should be interpreted as relative
            if chromosome is not None:
                self.chromosome = chromosome
            # If a chromosome if not provided, the position should be interpreted as absolute
            else:
                self.chromosome, self.position = parse_genomic_coordinate(position)
        else:
            raise ValueError('Provided data could not be decoded into a valid genomic coordinate')

        # Process data further
        self.position = long(self.position)
        try:
            self.chromosome = int(self.chromosome)
        except ValueError:
            try:
                self.chromosome = self._reverse_chromosomes[str(self.chromosome)]
            except KeyError:
                raise ValueError('Invalid chromosome was provided')

    def __str__(self):
        '''Human readable version of genomic coordinate as string.
        '''
        return self.as_locus()

    def __unicode__(self):
        '''Python 2 mapping for string invokation.
        '''
        return str(self)

    def as_locus(self):
        '''Returns coordinates in locus format <CHROMOSOME>:<POSITION>.
        '''
        return '%(chromosome)s:%(position)s' % {
            'chromosome': self.get_chromosome_display(),
            'position': self.position
        }

    def as_long(self):
        '''Returns bit-shifted long integer for locus.
        '''
        ret = self.chromosome << 28
        ret |= self.position
        return ret

    def get_chromosome_display(self):
        '''Converts higher number chromosomes to character representation.
        '''
        return self._forward_chromosomes[self.chromosome]
