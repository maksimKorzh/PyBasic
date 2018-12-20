#! /usr/bin/python

"""This class defines an object that can be returned by the BASICParser to
indicate the need for a control flow branch. The information within the
object tells the Program the nature of the jump and therefore whether a
return address need to be added to the return stack.

>>> flowsignal = FlowSignal(ftype=FlowSignal.RETURN)
>>> print(flowsignal.ftarget)
-1
>>> flowsignal = FlowSignal(ftarget=100, ftype=FlowSignal.SIMPLE_JUMP)
>>> print(flowsignal.ftarget)
100
>>> print(flowsignal.ftype)
0
"""


class FlowSignal:

    # Jump categories

    # Indicates a simple jump as the result
    # of a GOTO or conditional branch. The
    # ftarget value should be the jump target, i.e.
    # the line number being jumped to
    SIMPLE_JUMP        = 0

    # Indicates a subroutine call where the
    # return address must be the line number of the instruction
    # of the following the call.
    # The ftarget value should be the line number of the first line
    # of the subroutine
    GOSUB              = 1

    # Indicates the start of a FOR loop where loop
    # variable has not reached the end value, and therefore the loop
    # must be repeated. There should be therefore be
    # no ftarget value associated with it
    LOOP_BEGIN         = 2

    # An indication from a processed NEXT statement that the loop is to
    # be repeated. Since the return address is already on the stack,
    # there does not need to be an ftarget value associated with the signal.
    LOOP_REPEAT        = 3

    # An indication from a processed NEXT statement that the loop must
    # terminate. The next instruction to execute will be the one following
    # the NEXT statement, so there should be
    # no ftarget value specified
    LOOP_END           = 4

    # An indication from a FOR statement that the loop should be skipped because
    # loop variable has reached its end value. The ftarget should be
    # the loop variable to look for in the terminating NEXT statement
    LOOP_SKIP          = 5

    # Indicates a subroutine return has been processed, where the return
    # address is on the return stack. There should be therefore
    # be no ftarget value specified
    RETURN             = 6

    # Indicates that execution should cease because a stop statement has
    # been processed. There should be therefore be no ftarget value specified
    STOP               = 7

    def __init__(self, ftarget=None, ftype=SIMPLE_JUMP):
        """Creates a new FlowSignal for a branch. If the jump
        target is supplied, then the branch is assumed to be
        either a GOTO or conditional branch and the type is assigned as
        SIMPLE_JUMP. If no jump_target is supplied, then a jump_type must be
        supplied, which must either be GOSUB, RETURN, LOOP_BEGIN,
        LOOP_END, LOOP_REPEAT, LOOP_SKIP or STOP. In the latter cases
        the jump target is assigned an arbitrary value of None.

        :param ftarget: The associated value
        :param ftype: Either GOSUB, SIMPLE_JUMP, RETURN, LOOP_BEGIN,
        LOOP_SKIP, LOOP_END or STOP
        """

        if ftype not in [self.GOSUB, self.SIMPLE_JUMP, self.LOOP_BEGIN,
                         self.LOOP_REPEAT, self.LOOP_END, self.RETURN,
                         self.LOOP_SKIP, self.STOP]:
            raise TypeError("Invalid flow signal type supplied: " + str(ftype))

        if ftarget == None and \
           ftype in [self.SIMPLE_JUMP, self.GOSUB, self.LOOP_SKIP]:
            raise TypeError("Invalid jump target supplied for flow signal type: " + str(ftarget))

        if ftarget != None and \
           ftype in [self.RETURN, self.LOOP_BEGIN, self.LOOP_REPEAT,
                     self.LOOP_END, self.STOP]:
            raise TypeError("Target wrongly supplied for flow signal " + str(ftype))

        self.ftype = ftype
        self.ftarget = ftarget

