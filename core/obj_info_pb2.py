# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: obj_info.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2
from . import roadmap_pb2 as roadmap__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='obj_info.proto',
  package='obj_info',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0eobj_info.proto\x12\x08obj_info\x1a\x0c\x63ommon.proto\x1a\rroadmap.proto\"\xec\x02\n\rPerceptionObj\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08is_valid\x18\x02 \x01(\x08\x12\t\n\x01x\x18\x03 \x01(\x01\x12\t\n\x01y\x18\x04 \x01(\x01\x12\r\n\x05theta\x18\x05 \x01(\x02\x12\x0b\n\x03vel\x18\x06 \x01(\x02\x12\x11\n\tvel_theta\x18\x07 \x01(\x02\x12\x0b\n\x03\x61\x63\x63\x18\x08 \x01(\x02\x12\x0e\n\x06radius\x18\t \x01(\x02\x12\x13\n\x0bmotion_conf\x18\n \x01(\x02\x12\x15\n\rposition_conf\x18\x0b \x01(\x02\x12\x11\n\tkind_conf\x18\x0c \x01(\x02\x12\x31\n\x0craw_obj_kind\x18\r \x01(\x0e\x32\x1b.obj_info.PerceptionObjKind\x12\x15\n\rmoving_status\x18\x0e \x01(\r\x12\x12\n\nis_tracked\x18\x0f \x01(\r\x12\x17\n\x0ftotal_point_num\x18\x10 \x01(\r\x12%\n\x0cvertex_point\x18\x11 \x03(\x0b\x32\x0f.common.Point3d\"n\n\x14PredictionTrajectory\x12 \n\npred_poses\x18\x01 \x03(\x0b\x32\x0c.common.Pose\x12\x34\n\rpred_lane_seq\x18\x02 \x01(\x0b\x32\x1d.roadmap.LaneSequenceInternal\"\xce\x01\n\x17ObjCollisionInfoHistory\x12\x1a\n\x12\x63ollision_traj_num\x18\x01 \x01(\x05\x12\x31\n\x12\x63ollision_lane_seq\x18\x02 \x03(\x0b\x32\x15.roadmap.LaneSequence\x12\x15\n\rhas_collision\x18\x03 \x03(\x08\x12\x1d\n\x15\x65go_to_collision_dist\x18\x04 \x03(\x01\x12\x1d\n\x15obj_to_collision_dist\x18\x05 \x03(\x01\x12\x0f\n\x07\x65go_vel\x18\x06 \x01(\x01\"`\n\nObjHistory\x12\x0e\n\x06obj_id\x18\x01 \x01(\x05\x12\x42\n\x17obj_collision_info_hist\x18\x02 \x01(\x0b\x32!.obj_info.ObjCollisionInfoHistory\"H\n\rObjHistorySet\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12)\n\x0bhistory_set\x18\x02 \x03(\x0b\x32\x14.obj_info.ObjHistory\"d\n\x0ePerceptionData\x12\x1d\n\x15is_mov_obj_list_valid\x18\x01 \x01(\x08\x12\x0c\n\x04size\x18\x02 \x01(\x05\x12%\n\x04objs\x18\x03 \x03(\x0b\x32\x17.obj_info.PerceptionObj\"M\n\x0eObjBasePolygon\x12-\n\x11obj_base_polygons\x18\x01 \x03(\x0b\x32\x12.common.ObjPolygon\x12\x0c\n\x04size\x18\x02 \x01(\x05\"\xa3\x01\n\x07ObjInfo\x12\x31\n\x0fperception_data\x18\x01 \x01(\x0b\x32\x18.obj_info.PerceptionData\x12\x30\n\x0fobj_history_set\x18\x02 \x01(\x0b\x32\x17.obj_info.ObjHistorySet\x12\x33\n\x11obj_base_polygons\x18\x03 \x01(\x0b\x32\x18.obj_info.ObjBasePolygon*\xdb\x01\n\x11PerceptionObjKind\x12\x07\n\x03\x43\x41R\x10\x00\x12\t\n\x05TRUCK\x10\x01\x12\x07\n\x03\x42US\x10\x02\x12\x0b\n\x07\x42ICYCLE\x10\x03\x12\x10\n\x0cTRIPLE_WHEEL\x10\x04\x12\t\n\x05HUMAN\x10\x05\x12\n\n\x06\x41NIMAL\x10\x06\x12\t\n\x05OTHER\x10\x07\x12\x08\n\x04LINE\x10\x08\x12\t\n\x05RADAR\x10\t\x12\t\n\x05\x44OLLY\x10\n\x12\x08\n\x04\x43ONE\x10\x0b\x12\x08\n\x04\x42IRD\x10\x0c\x12\x0e\n\nFIRE_TRUCK\x10\r\x12\x0b\n\x07TRAILER\x10\x0e\x12\x07\n\x03\x41GV\x10\x0f\x12\x0e\n\nBLIND_AREA\x10\x10\x62\x06proto3'
  ,
  dependencies=[common__pb2.DESCRIPTOR,roadmap__pb2.DESCRIPTOR,])

_PERCEPTIONOBJKIND = _descriptor.EnumDescriptor(
  name='PerceptionObjKind',
  full_name='obj_info.PerceptionObjKind',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CAR', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRUCK', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BUS', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BICYCLE', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRIPLE_WHEEL', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HUMAN', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ANIMAL', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OTHER', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LINE', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RADAR', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DOLLY', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CONE', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BIRD', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FIRE_TRUCK', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TRAILER', index=14, number=14,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='AGV', index=15, number=15,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BLIND_AREA', index=16, number=16,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1265,
  serialized_end=1484,
)
_sym_db.RegisterEnumDescriptor(_PERCEPTIONOBJKIND)

PerceptionObjKind = enum_type_wrapper.EnumTypeWrapper(_PERCEPTIONOBJKIND)
CAR = 0
TRUCK = 1
BUS = 2
BICYCLE = 3
TRIPLE_WHEEL = 4
HUMAN = 5
ANIMAL = 6
OTHER = 7
LINE = 8
RADAR = 9
DOLLY = 10
CONE = 11
BIRD = 12
FIRE_TRUCK = 13
TRAILER = 14
AGV = 15
BLIND_AREA = 16



_PERCEPTIONOBJ = _descriptor.Descriptor(
  name='PerceptionObj',
  full_name='obj_info.PerceptionObj',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='obj_info.PerceptionObj.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_valid', full_name='obj_info.PerceptionObj.is_valid', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='x', full_name='obj_info.PerceptionObj.x', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='obj_info.PerceptionObj.y', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='theta', full_name='obj_info.PerceptionObj.theta', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vel', full_name='obj_info.PerceptionObj.vel', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vel_theta', full_name='obj_info.PerceptionObj.vel_theta', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acc', full_name='obj_info.PerceptionObj.acc', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='obj_info.PerceptionObj.radius', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='motion_conf', full_name='obj_info.PerceptionObj.motion_conf', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='position_conf', full_name='obj_info.PerceptionObj.position_conf', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kind_conf', full_name='obj_info.PerceptionObj.kind_conf', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw_obj_kind', full_name='obj_info.PerceptionObj.raw_obj_kind', index=12,
      number=13, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='moving_status', full_name='obj_info.PerceptionObj.moving_status', index=13,
      number=14, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='is_tracked', full_name='obj_info.PerceptionObj.is_tracked', index=14,
      number=15, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_point_num', full_name='obj_info.PerceptionObj.total_point_num', index=15,
      number=16, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vertex_point', full_name='obj_info.PerceptionObj.vertex_point', index=16,
      number=17, type=11, cpp_type=10, label=3,
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
  serialized_start=58,
  serialized_end=422,
)


_PREDICTIONTRAJECTORY = _descriptor.Descriptor(
  name='PredictionTrajectory',
  full_name='obj_info.PredictionTrajectory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pred_poses', full_name='obj_info.PredictionTrajectory.pred_poses', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pred_lane_seq', full_name='obj_info.PredictionTrajectory.pred_lane_seq', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=424,
  serialized_end=534,
)


_OBJCOLLISIONINFOHISTORY = _descriptor.Descriptor(
  name='ObjCollisionInfoHistory',
  full_name='obj_info.ObjCollisionInfoHistory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='collision_traj_num', full_name='obj_info.ObjCollisionInfoHistory.collision_traj_num', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='collision_lane_seq', full_name='obj_info.ObjCollisionInfoHistory.collision_lane_seq', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='has_collision', full_name='obj_info.ObjCollisionInfoHistory.has_collision', index=2,
      number=3, type=8, cpp_type=7, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ego_to_collision_dist', full_name='obj_info.ObjCollisionInfoHistory.ego_to_collision_dist', index=3,
      number=4, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='obj_to_collision_dist', full_name='obj_info.ObjCollisionInfoHistory.obj_to_collision_dist', index=4,
      number=5, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ego_vel', full_name='obj_info.ObjCollisionInfoHistory.ego_vel', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=537,
  serialized_end=743,
)


_OBJHISTORY = _descriptor.Descriptor(
  name='ObjHistory',
  full_name='obj_info.ObjHistory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='obj_id', full_name='obj_info.ObjHistory.obj_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='obj_collision_info_hist', full_name='obj_info.ObjHistory.obj_collision_info_hist', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=745,
  serialized_end=841,
)


_OBJHISTORYSET = _descriptor.Descriptor(
  name='ObjHistorySet',
  full_name='obj_info.ObjHistorySet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='obj_info.ObjHistorySet.size', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='history_set', full_name='obj_info.ObjHistorySet.history_set', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=843,
  serialized_end=915,
)


_PERCEPTIONDATA = _descriptor.Descriptor(
  name='PerceptionData',
  full_name='obj_info.PerceptionData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='is_mov_obj_list_valid', full_name='obj_info.PerceptionData.is_mov_obj_list_valid', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='obj_info.PerceptionData.size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='objs', full_name='obj_info.PerceptionData.objs', index=2,
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
  serialized_start=917,
  serialized_end=1017,
)


_OBJBASEPOLYGON = _descriptor.Descriptor(
  name='ObjBasePolygon',
  full_name='obj_info.ObjBasePolygon',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='obj_base_polygons', full_name='obj_info.ObjBasePolygon.obj_base_polygons', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='obj_info.ObjBasePolygon.size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=1019,
  serialized_end=1096,
)


_OBJINFO = _descriptor.Descriptor(
  name='ObjInfo',
  full_name='obj_info.ObjInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='perception_data', full_name='obj_info.ObjInfo.perception_data', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='obj_history_set', full_name='obj_info.ObjInfo.obj_history_set', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='obj_base_polygons', full_name='obj_info.ObjInfo.obj_base_polygons', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=1099,
  serialized_end=1262,
)

_PERCEPTIONOBJ.fields_by_name['raw_obj_kind'].enum_type = _PERCEPTIONOBJKIND
_PERCEPTIONOBJ.fields_by_name['vertex_point'].message_type = common__pb2._POINT3D
_PREDICTIONTRAJECTORY.fields_by_name['pred_poses'].message_type = common__pb2._POSE
_PREDICTIONTRAJECTORY.fields_by_name['pred_lane_seq'].message_type = roadmap__pb2._LANESEQUENCEINTERNAL
_OBJCOLLISIONINFOHISTORY.fields_by_name['collision_lane_seq'].message_type = roadmap__pb2._LANESEQUENCE
_OBJHISTORY.fields_by_name['obj_collision_info_hist'].message_type = _OBJCOLLISIONINFOHISTORY
_OBJHISTORYSET.fields_by_name['history_set'].message_type = _OBJHISTORY
_PERCEPTIONDATA.fields_by_name['objs'].message_type = _PERCEPTIONOBJ
_OBJBASEPOLYGON.fields_by_name['obj_base_polygons'].message_type = common__pb2._OBJPOLYGON
_OBJINFO.fields_by_name['perception_data'].message_type = _PERCEPTIONDATA
_OBJINFO.fields_by_name['obj_history_set'].message_type = _OBJHISTORYSET
_OBJINFO.fields_by_name['obj_base_polygons'].message_type = _OBJBASEPOLYGON
DESCRIPTOR.message_types_by_name['PerceptionObj'] = _PERCEPTIONOBJ
DESCRIPTOR.message_types_by_name['PredictionTrajectory'] = _PREDICTIONTRAJECTORY
DESCRIPTOR.message_types_by_name['ObjCollisionInfoHistory'] = _OBJCOLLISIONINFOHISTORY
DESCRIPTOR.message_types_by_name['ObjHistory'] = _OBJHISTORY
DESCRIPTOR.message_types_by_name['ObjHistorySet'] = _OBJHISTORYSET
DESCRIPTOR.message_types_by_name['PerceptionData'] = _PERCEPTIONDATA
DESCRIPTOR.message_types_by_name['ObjBasePolygon'] = _OBJBASEPOLYGON
DESCRIPTOR.message_types_by_name['ObjInfo'] = _OBJINFO
DESCRIPTOR.enum_types_by_name['PerceptionObjKind'] = _PERCEPTIONOBJKIND
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PerceptionObj = _reflection.GeneratedProtocolMessageType('PerceptionObj', (_message.Message,), {
  'DESCRIPTOR' : _PERCEPTIONOBJ,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.PerceptionObj)
  })
_sym_db.RegisterMessage(PerceptionObj)

PredictionTrajectory = _reflection.GeneratedProtocolMessageType('PredictionTrajectory', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTIONTRAJECTORY,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.PredictionTrajectory)
  })
_sym_db.RegisterMessage(PredictionTrajectory)

ObjCollisionInfoHistory = _reflection.GeneratedProtocolMessageType('ObjCollisionInfoHistory', (_message.Message,), {
  'DESCRIPTOR' : _OBJCOLLISIONINFOHISTORY,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.ObjCollisionInfoHistory)
  })
_sym_db.RegisterMessage(ObjCollisionInfoHistory)

ObjHistory = _reflection.GeneratedProtocolMessageType('ObjHistory', (_message.Message,), {
  'DESCRIPTOR' : _OBJHISTORY,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.ObjHistory)
  })
_sym_db.RegisterMessage(ObjHistory)

ObjHistorySet = _reflection.GeneratedProtocolMessageType('ObjHistorySet', (_message.Message,), {
  'DESCRIPTOR' : _OBJHISTORYSET,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.ObjHistorySet)
  })
_sym_db.RegisterMessage(ObjHistorySet)

PerceptionData = _reflection.GeneratedProtocolMessageType('PerceptionData', (_message.Message,), {
  'DESCRIPTOR' : _PERCEPTIONDATA,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.PerceptionData)
  })
_sym_db.RegisterMessage(PerceptionData)

ObjBasePolygon = _reflection.GeneratedProtocolMessageType('ObjBasePolygon', (_message.Message,), {
  'DESCRIPTOR' : _OBJBASEPOLYGON,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.ObjBasePolygon)
  })
_sym_db.RegisterMessage(ObjBasePolygon)

ObjInfo = _reflection.GeneratedProtocolMessageType('ObjInfo', (_message.Message,), {
  'DESCRIPTOR' : _OBJINFO,
  '__module__' : 'obj_info_pb2'
  # @@protoc_insertion_point(class_scope:obj_info.ObjInfo)
  })
_sym_db.RegisterMessage(ObjInfo)


# @@protoc_insertion_point(module_scope)
