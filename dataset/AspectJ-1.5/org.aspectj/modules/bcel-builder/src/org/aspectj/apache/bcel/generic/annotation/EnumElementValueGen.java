/* *******************************************************************
 * Copyright (c) 2004 IBM
 * All rights reserved. 
 * This program and the accompanying materials are made available 
 * under the terms of the Eclipse Public License v1.0 
 * which accompanies this distribution and is available at 
 * http://www.eclipse.org/legal/epl-v10.html 
 *  
 * Contributors: 
 *     Andy Clement -     initial implementation {date}
 * ******************************************************************/

package org.aspectj.apache.bcel.generic.annotation;

import java.io.DataOutputStream;
import java.io.IOException;

import org.aspectj.apache.bcel.classfile.ConstantUtf8;
import org.aspectj.apache.bcel.classfile.annotation.ElementValue;
import org.aspectj.apache.bcel.classfile.annotation.EnumElementValue;
import org.aspectj.apache.bcel.generic.ConstantPoolGen;
import org.aspectj.apache.bcel.generic.ObjectType;


public class EnumElementValueGen extends ElementValueGen {
	
	// For enum types, these two indices point to the type and value
	private int typeIdx;
	private int valueIdx;
	
	/**
	 * This ctor assumes the constant pool already contains the right type and value -
	 * as indicated by typeIdx and valueIdx.  This ctor is used for deserialization
	 */
    protected EnumElementValueGen(int typeIdx,int valueIdx,ConstantPoolGen cpool) {
    	super(ElementValueGen.ENUM_CONSTANT,cpool);
    	if (type != ENUM_CONSTANT) 
    		throw new RuntimeException("Only element values of type enum can be built with this ctor");
    	this.typeIdx = typeIdx;
    	this.valueIdx= valueIdx;
    }
	
	/**
     * Return immutable variant of this EnumElementValue
     */
	public ElementValue getElementValue() {
		System.err.println("Duplicating value: "+getEnumTypeString()+":"+getEnumValueString());
		return new EnumElementValue(type,typeIdx,valueIdx,cpGen.getConstantPool());
	}
    
    public EnumElementValueGen(ObjectType t,String value,ConstantPoolGen cpool) {
    	super(ElementValueGen.ENUM_CONSTANT,cpool);
    	typeIdx = cpool.addUtf8(t.getSignature());// was addClass(t);
    	valueIdx= cpool.addUtf8(value);// was addString(value);
    }

	public EnumElementValueGen(EnumElementValue value, ConstantPoolGen cpool, boolean copyPoolEntries) {
		super(ENUM_CONSTANT,cpool);
		if (copyPoolEntries) {
			typeIdx = cpool.addUtf8(value.getEnumTypeString());// was addClass(value.getEnumTypeString());
			valueIdx = cpool.addUtf8(value.getEnumValueString()); // was addString(value.getEnumValueString());
		} else {
			typeIdx  = value.getTypeIndex();
			valueIdx = value.getValueIndex();
		}
	}

	public void dump(DataOutputStream dos) throws IOException {
    	dos.writeByte(type);      // u1 type of value (ENUM_CONSTANT == 'e')
		dos.writeShort(typeIdx);  // u2
		dos.writeShort(valueIdx); // u2
    }
    
    public String stringifyValue() {
    	ConstantUtf8 cu8 = (ConstantUtf8)getConstantPool().getConstant(valueIdx);
		return cu8.getBytes();
//    	ConstantString cu8 = (ConstantString)getConstantPool().getConstant(valueIdx);
//    	return ((ConstantUtf8)getConstantPool().getConstant(cu8.getStringIndex())).getBytes();
    }
    
    
    // BCELBUG: Should we need to call utility.signatureToString() on the output here?
    public String getEnumTypeString() {
//		Constant cc = getConstantPool().getConstant(typeIdx);
//    	ConstantClass cu8 = (ConstantClass)getConstantPool().getConstant(typeIdx);		
//    	return ((ConstantUtf8)getConstantPool().getConstant(cu8.getNameIndex())).getBytes();
		return ((ConstantUtf8)getConstantPool().getConstant(typeIdx)).getBytes();
		// return Utility.signatureToString(cu8.getBytes());
    }
    
	public String getEnumValueString() {
		return ((ConstantUtf8)getConstantPool().getConstant(valueIdx)).getBytes();
//		ConstantString cu8 = (ConstantString)getConstantPool().getConstant(valueIdx);
//    	return ((ConstantUtf8)getConstantPool().getConstant(cu8.getStringIndex())).getBytes();
	}
    
    public int getValueIndex() { return valueIdx;}
    public int getTypeIndex()  { return typeIdx; }

   
}
