# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: prediction_input.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import obj_info_pb2 as obj__info__pb2
from . import ego_info_pb2 as ego__info__pb2
from . import map_input_info_pb2 as map__input__info__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='prediction_input.proto',
  package='prediction_input',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16prediction_input.proto\x12\x10prediction_input\x1a\x0eobj_info.proto\x1a\x0e\x65go_info.proto\x1a\x14map_input_info.proto\"k\n\x14PredictionExtraInput\x12\x0f\n\x07obj_num\x18\x01 \x01(\x05\x12\x17\n\x0fmov_obj_id_list\x18\x02 \x03(\x05\x12\x16\n\x0eplay_cur_frame\x18\x03 \x01(\x05\x12\x11\n\treplay_ts\x18\x04 \x01(\x04\"\xff\x01\n\x0fPredictionInput\x12#\n\x08obj_info\x18\x01 \x01(\x0b\x32\x11.obj_info.ObjInfo\x12#\n\x08\x65go_info\x18\x02 \x01(\x0b\x32\x11.ego_info.EgoInfo\x12\x38\n\x10near_segment_set\x18\x03 \x01(\x0b\x32\x1e.map_input_info.NearSegmentSet\x12+\n\tego_route\x18\x04 \x01(\x0b\x32\x18.map_input_info.EgoRoute\x12;\n\x0b\x65xtra_input\x18\x05 \x01(\x0b\x32&.prediction_input.PredictionExtraInputb\x06proto3'
  ,
  dependencies=[obj__info__pb2.DESCRIPTOR,ego__info__pb2.DESCRIPTOR,map__input__info__pb2.DESCRIPTOR,])




_PREDICTIONEXTRAINPUT = _descriptor.Descriptor(
  name='PredictionExtraInput',
  full_name='prediction_input.PredictionExtraInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='obj_num', full_name='prediction_input.PredictionExtraInput.obj_num', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mov_obj_id_list', full_name='prediction_input.PredictionExtraInput.mov_obj_id_list', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='play_cur_frame', full_name='prediction_input.PredictionExtraInput.play_cur_frame', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='replay_ts', full_name='prediction_input.PredictionExtraInput.replay_ts', index=3,
      number=4, type=4, cpp_type=4, label=1,
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
  serialized_start=98,
  serialized_end=205,
)


_PREDICTIONINPUT = _descriptor.Descriptor(
  name='PredictionInput',
  full_name='prediction_input.PredictionInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='obj_info', full_name='prediction_input.PredictionInput.obj_info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ego_info', full_name='prediction_input.PredictionInput.ego_info', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='near_segment_set', full_name='prediction_input.PredictionInput.near_segment_set', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ego_route', full_name='prediction_input.PredictionInput.ego_route', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extra_input', full_name='prediction_input.PredictionInput.extra_input', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
  serialized_start=208,
  serialized_end=463,
)

_PREDICTIONINPUT.fields_by_name['obj_info'].message_type = obj__info__pb2._OBJINFO
_PREDICTIONINPUT.fields_by_name['ego_info'].message_type = ego__info__pb2._EGOINFO
_PREDICTIONINPUT.fields_by_name['near_segment_set'].message_type = map__input__info__pb2._NEARSEGMENTSET
_PREDICTIONINPUT.fields_by_name['ego_route'].message_type = map__input__info__pb2._EGOROUTE
_PREDICTIONINPUT.fields_by_name['extra_input'].message_type = _PREDICTIONEXTRAINPUT
DESCRIPTOR.message_types_by_name['PredictionExtraInput'] = _PREDICTIONEXTRAINPUT
DESCRIPTOR.message_types_by_name['PredictionInput'] = _PREDICTIONINPUT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PredictionExtraInput = _reflection.GeneratedProtocolMessageType('PredictionExtraInput', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTIONEXTRAINPUT,
  '__module__' : 'prediction_input_pb2'
  # @@protoc_insertion_point(class_scope:prediction_input.PredictionExtraInput)
  })
_sym_db.RegisterMessage(PredictionExtraInput)

PredictionInput = _reflection.GeneratedProtocolMessageType('PredictionInput', (_message.Message,), {
  'DESCRIPTOR' : _PREDICTIONINPUT,
  '__module__' : 'prediction_input_pb2'
  # @@protoc_insertion_point(class_scope:prediction_input.PredictionInput)
  })
_sym_db.RegisterMessage(PredictionInput)


# @@protoc_insertion_point(module_scope)