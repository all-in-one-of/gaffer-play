##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

import unittest

import IECore

import Gaffer
import GafferScene
import GafferSceneTest

class SceneNodeTest( unittest.TestCase ) :

	def testRootConstraints( self ) :
	
		# we don't allow the root of the scene ("/") to carry objects, transforms,
		# or attributes. if we did, then there wouldn't be a sensible way of merging
		# them (particularly transforms) when a Group node has multiple inputs.
		# it's also pretty confusing to have stuff go on at the root level,
		# particularly as the root isn't well represented in the SceneEditor,
		# and applications like maya don't have stuff happening at the root
		# level either. we achieve this by having the SceneNode simply not
		# call the various processing functions for the root.
		
		node = GafferSceneTest.CompoundObjectSource()
		node["in"].setValue(
			IECore.CompoundObject( {
				"object" : IECore.SpherePrimitive()
			} )
		)
		
		self.assertEqual( node["out"].object( "/" ), None )
		
		node = GafferSceneTest.CompoundObjectSource()
		node["in"].setValue(
			IECore.CompoundObject( {
				"transform" : IECore.M44fData( IECore.M44f.createTranslated( IECore.V3f( 1 ) ) )
			} )
		)
		
		self.assertEqual( node["out"].transform( "/" ), IECore.M44f() )
		
		node = GafferSceneTest.CompoundObjectSource()
		node["in"].setValue(
			IECore.CompoundObject( {
				"attributes" : IECore.CompoundObject()
			} )
		)
		
		self.assertEqual( node["out"].attributes( "/" ), None )
	
if __name__ == "__main__":
	unittest.main()