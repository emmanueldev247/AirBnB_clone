#!/usr/bin/python3
# Created by Israel Udofia & Emmanuel Ademola

"""Unittest for base_model.py"""

import unittest
import models
from models.base_model import BaseModel
from datetime import datetime
from time import sleep


class TestBaseModelClass(unittest.TestCase):
    """Test suites"""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_uuid(self):
        BM1 = BaseModel()
        BM2 = BaseModel()

        self.assertIsInstance(BM1, BaseModel)
        self.assertTrue(hasattr(BM1, "id"))
        self.assertNotEqual(BM1.id, BM2.id)
        self.assertIsInstance(BM1.id, str)

    def test_created_at(self):
        BM1 = BaseModel()

        self.assertTrue(hasattr(BM1, "created_at"))
        self.assertIsInstance(BM1.created_at, datetime)

    def test_updated_at(self):
        BM1 = BaseModel()

        self.assertTrue(hasattr(BM1, "updated_at"))
        self.assertIsInstance(BM1.updated_at, datetime)

    def test_save_method(self):
        model = BaseModel()
        initial_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(model.updated_at, initial_updated_at)

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_two_models_created_at(self):
        bm1 = BaseModel()
        sleep(0.1)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)
        self.assertNotEqual(bm1.created_at, bm2.created_at)

    def test_two_models_updated_at(self):
        bm1 = BaseModel()
        sleep(0.1)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)
        self.assertNotEqual(bm1.updated_at, bm2.updated_at)

    def test_fixed_id(self):
        bm1 = BaseModel()
        bm1.id = '123'
        self.assertEqual(bm1.id, '123')

    def test_to_dict(self):
        bm1 = BaseModel()
        model_dict = bm1.to_dict()

        self.assertIn('__class__', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bmstr = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_args_unused(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_serialization_and_deserialization(self):
        # I got this from the intranet example (task 3)
        my_model = BaseModel()
        my_model.name = "My_First_Model"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        my_new_model_json = my_new_model.to_dict()
        self.assertEqual(my_model_json, my_new_model_json)


if __name__ == '__main__':
    unittest.main()
