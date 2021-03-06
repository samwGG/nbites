/**
* @file TeamInfo.h
* The file declares a class that encapsulates the structure TeamInfo defined in
* the file RoboCupGameControlData.h that is provided with the GameController.
* @author <a href="mailto:Thomas.Roefer@dfki.de">Thomas Röfer</a>
*/

#pragma once

#include "RoboCupGameControlData.h"
#include "Tools/Streams/Streamable.h"

class TeamInfoBH : public TeamInfo, public Streamable
{
private:
  /**
  * The method makes the object streamable.
  * @param in The stream from which the object is read (if in != 0).
  * @param out The stream to which the object is written (if out != 0).
  */
  virtual void serialize(In* in, Out* out);

public:
  /** Default constructor. */
  TeamInfoBH();

  /** Draws the score in the scene view. */
  virtual void draw() const;
};

class OwnTeamInfoBH : public TeamInfoBH
{
public:
  OwnTeamInfoBH();
  virtual void draw() const;

};

class OpponentTeamInfoBH : public TeamInfoBH
{
public:
  OpponentTeamInfoBH();
};
