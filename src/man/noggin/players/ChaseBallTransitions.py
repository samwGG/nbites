import man.motion.SweetMoves as SweetMoves
import man.motion.HeadMoves as HeadMoves
import ChaseBallConstants as constants
import KickingHelpers as helpers
from .. import NogginConstants
from ..playbook.PBConstants import GOALIE

from math import fabs

####### CHASING STUFF ##############

def shouldChaseBall(player):
    """
    We see the ball. So go get it.
    """
    ball = player.brain.ball
    return (ball.on)

def shouldApproachBall(player):
    """
    Approach the ball if it is far away.
    """
    ball = player.brain.ball
    return (ball.on and not shouldPositionForKick(player))

def shouldChaseFromPositionForKick(player):
    """
    Exit PFK if the ball is too far away.
    """
    ball = player.brain.ball
    return shouldChaseBall(player) and \
        not shouldPositionForKick(player) and \
        ball.dist > constants.BALL_PFK_MAX_X+10

def shouldPositionForKick(player):
    """
    Should begin aligning on the ball for a kick when close
    """
    ball = player.brain.ball
    return (constants.BALL_PFK_LEFT_Y > ball.relY > \
            constants.BALL_PFK_RIGHT_Y and \
            constants.BALL_PFK_MAX_X > ball.relX > \
            constants.BALL_PFK_MIN_X and \
            fabs(ball.bearing) < constants.BALL_PFK_BEARING_THRESH)

def shouldStopAndKick(player):
    """
    Ball is in the correct position to kick but we aren't stopped
    """
    ball = player.brain.ball
    return ball.on and \
        ball.relX > constants.SHOULD_KICK_CLOSE_X and \
        ball.relX < constants.SHOULD_KICK_FAR_X and \
        fabs(ball.relY) < constants.SHOULD_KICK_Y
        # and player.counter < 1 ??

def shouldKickNow(player):
    """
    Ball is in the correct position to kick and we are stopped
    """
    ball = player.brain.ball
    # Ensure we are stopped, we see the ball,
    # and the ball is in the "kicking region"
    return player.brain.nav.isStopped() and \
        ball.on and \
        ball.relX > constants.SHOULD_KICK_CLOSE_X and \
        ball.relX < constants.SHOULD_KICK_FAR_X and \
        fabs(ball.relY) < constants.SHOULD_KICK_Y
        # and player.counter < 1 ??

def shouldDribble(player):
    """
    Ball is in between us and the opp goal, let's dribble for a while
    """
    if constants.USE_DRIBBLE:
        my = player.brain.my
        dribbleAimPoint = helpers.getShotCloseAimPoint(player)
        goalBearing = my.getRelativeBearing(dribbleAimPoint)
        return  (not player.penaltyKicking and
                 0 < player.brain.ball.relX < constants.SHOULD_DRIBBLE_X and
                 0 < fabs(player.brain.ball.relY) < constants.SHOULD_DRIBBLE_Y and
                 fabs(goalBearing) < constants.SHOULD_DRIBBLE_BEARING and
                 not player.brain.my.inOppGoalbox() and
                 player.brain.my.x > (
                     NogginConstants.FIELD_WHITE_WIDTH / 3.0 +
                     NogginConstants.GREEN_PAD_X) )

def shouldStopDribbling(player):
    """
    While dribbling we should stop
    """
    my = player.brain.my
    dribbleAimPoint = helpers.getShotCloseAimPoint(player)
    goalBearing = my.getRelativeBearing(dribbleAimPoint)
    return (player.penaltyKicking or
            player.brain.my.inOppGoalbox() or
            player.brain.ball.relX > constants.STOP_DRIBBLE_X or
            fabs(player.brain.ball.relY) > constants.STOP_DRIBBLE_Y or
            fabs(goalBearing) > constants.STOP_DRIBBLE_BEARING or
            player.brain.my.x < ( NogginConstants.FIELD_WHITE_WIDTH / 3.0 +
                                  NogginConstants.GREEN_PAD_X))

####### FIND BALL STUFF ##############

def shouldScanFindBall(player):
    """
    We lost the ball, scan to find it
    """
    return (player.brain.ball.framesOff > constants.BALL_OFF_THRESH)

def shouldScanFindBallActiveLoc(player):
    """
    We lost the ball, scan to find it
    """
    return not (player.brain.tracker.activePanUp or
                player.brain.tracker.activePanOut) and \
        (player.brain.ball.framesOff > constants.BALL_OFF_ACTIVE_LOC_THRESH)

def shouldSpinFindBall(player):
    """
    Should spin if we already tried searching
    """
    return (player.stateTime >=
            SweetMoves.getMoveTime(HeadMoves.HIGH_SCAN_BALL))

def shouldSpinFindBallAgain(player):
    """
    If we have been walkFindBall-ing too long we should spin.
    """
    return player.stateTime > 300

def shouldntStopChasing(player):
    """
    Dont switch out of chaser in certain circumstances
    """
    return player.inKickingState

def shouldWalkFindBall(player):
    """
    If we've been spinFindBall-ing too long we should walk
    """
    return player.counter > constants.WALK_FIND_BALL_FRAMES_THRESH and \
        player.brain.ball.framesOff > constants.BALL_OFF_THRESH

def shouldPreKickScan(player):
    if player.brain.ball.on:
        return (constants.PRE_KICK_SCAN_MIN_DIST < player.brain.ball.dist
                < constants.PRE_KICK_SCAN_MAX_DIST and
                abs(player.brain.ball.bearing) <
                constants.APPROACH_ACTIVE_LOC_BEARING)
    return False

def shouldActiveLoc(player):
    if player.brain.ball.on:
        return (player.brain.ball.dist > constants.APPROACH_ACTIVE_LOC_DIST
                and fabs(player.brain.ball.bearing) <
                constants.APPROACH_ACTIVE_LOC_BEARING)

    else:
        return player.brain.ball.dist > constants.APPROACH_ACTIVE_LOC_DIST

def shouldStopPenaltyKickDribbling(player):
    """
    While dribbling we should stop
    """
    my = player.brain.my
    dribbleAimPoint = helpers.getShotCloseAimPoint(player)
    goalBearing = my.getRelativeBearing(dribbleAimPoint)
    return (inPenaltyKickStrikezone(player) or
            player.brain.ball.relX > constants.STOP_DRIBBLE_X or
            fabs(player.brain.ball.relY) > constants.STOP_DRIBBLE_Y or
            fabs(goalBearing) > constants.STOP_DRIBBLE_BEARING or
            player.counter > constants.STOP_PENALTY_DRIBBLE_COUNT)

def inPenaltyKickStrikezone(player):
    """
    If we are in a good place to kick
    """
    return (NogginConstants.OPP_GOALBOX_LEFT_X + 75. < player.brain.my.x)
