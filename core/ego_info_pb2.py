# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ego_info.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2
from . import roadmap_pb2 as roadmap__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ego_info.proto',
  package='ego_info',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0e\x65go_info.proto\x12\x08\x65go_info\x1a\x0c\x63ommon.proto\x1a\rroadmap.proto\"N\n\nTrajectory\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12\x15\n\rtruncated_idx\x18\x02 \x01(\x05\x12\x1b\n\x05poses\x18\x03 \x03(\x0b\x32\x0c.common.Pose\"\x95\x01\n\x07\x45goInfo\x12\x1e\n\x08\x65go_pose\x18\x01 \x01(\x0b\x32\x0c.common.Pose\x12\x0f\n\x07\x65go_vel\x18\x02 \x01(\x02\x12+\n\x0c\x65go_lane_seq\x18\x03 \x01(\x0b\x32\x15.roadmap.LaneSequence\x12,\n\x0e\x65go_traj_local\x18\x04 \x01(\x0b\x32\x14.ego_info.Trajectoryb\x06proto3'
  ,
  dependencies=[common__pb2.DESCRIPTOR,roadmap__pb2.DESCRIPTOR,])




_TRAJECTORY = _descriptor.Descriptor(
  name='Trajectory',
  full_name='ego_info.Trajectory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='ego_info.Trajectory.size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='truncated_idx', full_name='ego_info.Trajectory.truncated_idx', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='poses', full_name='ego_info.Trajectory.poses', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=135,
)


_EGOINFO = _descriptor.Descriptor(
  name='EgoInfo',
  full_name='ego_info.EgoInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ego_pose', full_name='ego_info.EgoInfo.ego_pose', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ego_vel', full_name='ego_info.EgoInfo.ego_vel', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ego_lane_seq', full_name='ego_info.EgoInfo.ego_lane_seq', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ego_traj_local', full_name='ego_info.EgoInfo.ego_traj_local', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=287,
)

_TRAJECTORY.fields_by_name['poses'].message_type = common__pb2._POSE
_EGOINFO.fields_by_name['ego_pose'].message_type = common__pb2._POSE
_EGOINFO.fields_by_name['ego_lane_seq'].message_type = roadmap__pb2._LANESEQUENCE
_EGOINFO.fields_by_name['ego_traj_local'].message_type = _TRAJECTORY
DESCRIPTOR.message_types_by_name['Trajectory'] = _TRAJECTORY
DESCRIPTOR.message_types_by_name['EgoInfo'] = _EGOINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Trajectory = _reflection.GeneratedProtocolMessageType('Trajectory', (_message.Message,), {
  'DESCRIPTOR' : _TRAJECTORY,
  '__module__' : 'ego_info_pb2'
  # @@protoc_insertion_point(class_scope:ego_info.Trajectory)
  })
_sym_db.RegisterMessage(Trajectory)

EgoInfo = _reflection.GeneratedProtocolMessageType('EgoInfo', (_message.Message,), {
  'DESCRIPTOR' : _EGOINFO,
  '__module__' : 'ego_info_pb2'
  # @@protoc_insertion_point(class_scope:ego_info.EgoInfo)
  })
_sym_db.RegisterMessage(EgoInfo)


# @@protoc_insertion_point(module_scope)
