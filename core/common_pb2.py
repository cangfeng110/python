# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='common.proto',
  package='common',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0c\x63ommon.proto\x12\x06\x63ommon\"\x1b\n\x03Pos\x12\t\n\x01x\x18\x01 \x01(\x01\x12\t\n\x01y\x18\x02 \x01(\x01\"/\n\x04Pose\x12\x18\n\x03pos\x18\x01 \x01(\x0b\x32\x0b.common.Pos\x12\r\n\x05theta\x18\x02 \x01(\x01\"*\n\x07Point3d\x12\t\n\x01x\x18\x01 \x01(\x01\x12\t\n\x01y\x18\x02 \x01(\x01\x12\t\n\x01z\x18\x03 \x01(\x01\"\xf3\x01\n\nObjPolygon\x12,\n\x04type\x18\x01 \x01(\x0e\x32\x1e.common.ObjPolygon.PolygonType\x12\x12\n\nvertex_num\x18\x02 \x01(\r\x12!\n\x08vertices\x18\x03 \x03(\x0b\x32\x0f.common.Point3d\x12\x1f\n\x06\x61xises\x18\x04 \x03(\x0b\x32\x0f.common.Point3d\x12\"\n\tcenter_pt\x18\x05 \x01(\x0b\x32\x0f.common.Point3d\x12\x0e\n\x06radius\x18\x06 \x01(\x01\"+\n\x0bPolygonType\x12\r\n\tARBITRARY\x10\x00\x12\r\n\tRECTANGLE\x10\x01\x62\x06proto3'
)



_OBJPOLYGON_POLYGONTYPE = _descriptor.EnumDescriptor(
  name='PolygonType',
  full_name='common.ObjPolygon.PolygonType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ARBITRARY', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RECTANGLE', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=347,
  serialized_end=390,
)
_sym_db.RegisterEnumDescriptor(_OBJPOLYGON_POLYGONTYPE)


_POS = _descriptor.Descriptor(
  name='Pos',
  full_name='common.Pos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='common.Pos.x', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='common.Pos.y', index=1,
      number=2, type=1, cpp_type=5, label=1,
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
  serialized_start=24,
  serialized_end=51,
)


_POSE = _descriptor.Descriptor(
  name='Pose',
  full_name='common.Pose',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pos', full_name='common.Pose.pos', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='theta', full_name='common.Pose.theta', index=1,
      number=2, type=1, cpp_type=5, label=1,
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
  serialized_start=53,
  serialized_end=100,
)


_POINT3D = _descriptor.Descriptor(
  name='Point3d',
  full_name='common.Point3d',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='common.Point3d.x', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='y', full_name='common.Point3d.y', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='z', full_name='common.Point3d.z', index=2,
      number=3, type=1, cpp_type=5, label=1,
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
  serialized_start=102,
  serialized_end=144,
)


_OBJPOLYGON = _descriptor.Descriptor(
  name='ObjPolygon',
  full_name='common.ObjPolygon',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='common.ObjPolygon.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vertex_num', full_name='common.ObjPolygon.vertex_num', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vertices', full_name='common.ObjPolygon.vertices', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='axises', full_name='common.ObjPolygon.axises', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='center_pt', full_name='common.ObjPolygon.center_pt', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='radius', full_name='common.ObjPolygon.radius', index=5,
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
    _OBJPOLYGON_POLYGONTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=390,
)

_POSE.fields_by_name['pos'].message_type = _POS
_OBJPOLYGON.fields_by_name['type'].enum_type = _OBJPOLYGON_POLYGONTYPE
_OBJPOLYGON.fields_by_name['vertices'].message_type = _POINT3D
_OBJPOLYGON.fields_by_name['axises'].message_type = _POINT3D
_OBJPOLYGON.fields_by_name['center_pt'].message_type = _POINT3D
_OBJPOLYGON_POLYGONTYPE.containing_type = _OBJPOLYGON
DESCRIPTOR.message_types_by_name['Pos'] = _POS
DESCRIPTOR.message_types_by_name['Pose'] = _POSE
DESCRIPTOR.message_types_by_name['Point3d'] = _POINT3D
DESCRIPTOR.message_types_by_name['ObjPolygon'] = _OBJPOLYGON
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Pos = _reflection.GeneratedProtocolMessageType('Pos', (_message.Message,), {
  'DESCRIPTOR' : _POS,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:common.Pos)
  })
_sym_db.RegisterMessage(Pos)

Pose = _reflection.GeneratedProtocolMessageType('Pose', (_message.Message,), {
  'DESCRIPTOR' : _POSE,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:common.Pose)
  })
_sym_db.RegisterMessage(Pose)

Point3d = _reflection.GeneratedProtocolMessageType('Point3d', (_message.Message,), {
  'DESCRIPTOR' : _POINT3D,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:common.Point3d)
  })
_sym_db.RegisterMessage(Point3d)

ObjPolygon = _reflection.GeneratedProtocolMessageType('ObjPolygon', (_message.Message,), {
  'DESCRIPTOR' : _OBJPOLYGON,
  '__module__' : 'common_pb2'
  # @@protoc_insertion_point(class_scope:common.ObjPolygon)
  })
_sym_db.RegisterMessage(ObjPolygon)


# @@protoc_insertion_point(module_scope)