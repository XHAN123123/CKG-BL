/*******************************************************************************
 * Copyright (c) 2000, 2005 IBM Corporation and others.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 * Contributors:
 *     IBM Corporation - initial API and implementation
 *******************************************************************************/
package org.aspectj.org.eclipse.jdt.core.dom;


public class AjASTMatcher extends ASTMatcher {
	
	/**
	 * Creates a new AST matcher instance.
	 * <p>
	 * For backwards compatibility, the matcher ignores tag
	 * elements below doc comments by default. Use 
	 * {@link #ASTMatcher(boolean) ASTMatcher(true)}
	 * for a matcher that compares doc tags by default.
	 * </p>
	 */
	public AjASTMatcher() {
		this(false);
	}

	/**
	 * Creates a new AST matcher instance.
	 * 
	 * @param matchDocTags <code>true</code> if doc comment tags are
	 * to be compared by default, and <code>false</code> otherwise
	 * @see #match(Javadoc,Object)
	 * @since 3.0
	 */
	public AjASTMatcher(boolean matchDocTags) {
		super(matchDocTags);
	}


	public boolean match(PointcutDeclaration node, Object other) {
		// ajh02: method added
		if (!(other instanceof PointcutDeclaration)) {
			return false;
		}
		PointcutDeclaration o = (PointcutDeclaration) other;
		int level = node.getAST().apiLevel;
		if (level == AST.JLS2_INTERNAL) {
			if (node.getModifiers() != o.getModifiers()) {
				return false;
			}
		}
		if (level >= AST.JLS3) {
			if (!safeSubtreeListMatch(node.modifiers(), o.modifiers())) {
				return false;
			}
		}
		return 
			safeSubtreeMatch(node.getJavadoc(), o.getJavadoc())
			&& safeSubtreeMatch(node.getName(), o.getName())
			&& safeSubtreeMatch(node.getDesignator(), o.getDesignator());
	}
	
	public boolean match(DefaultPointcut node, Object other) {
		return (other instanceof DefaultPointcut);
	}
	
	public boolean match(ReferencePointcut node, Object other) {
		if (!(other instanceof ReferencePointcut)) {
			return false;
		}
		ReferencePointcut o = (ReferencePointcut) other;
		int level = node.getAST().apiLevel;
		return safeSubtreeMatch(node.getName(), o.getName());
		// ajh02: will have to add something here when ReferencePointcuts are given
		// a list of Types for parameters
	}
	public boolean match(NotPointcut node, Object other) {
		if (!(other instanceof NotPointcut)) {
			return false;
		}
		NotPointcut o = (NotPointcut) other;
		return safeSubtreeMatch(node.getBody(), o.getBody());
	}
	public boolean match(PerObject node, Object other) {
		if (!(other instanceof PerObject)) {
			return false;
		}
		PerObject o = (PerObject) other;
		return safeSubtreeMatch(node.getBody(), o.getBody())
		&& o.isThis() == node.isThis();
	}
	public boolean match(PerCflow node, Object other) {
		if (!(other instanceof PerCflow)) {
			return false;
		}
		PerCflow o = (PerCflow) other;
		return safeSubtreeMatch(node.getBody(), o.getBody())
		&& node.isBelow() == o.isBelow();
	}
	public boolean match(PerTypeWithin node, Object other) {
		if (!(other instanceof PerTypeWithin)) {
			return false;
		}
		PerTypeWithin o = (PerTypeWithin) other;
		return true; // ajh02: stub, should look at the type pattern
	}
	public boolean match(CflowPointcut node, Object other) {
		if (!(other instanceof CflowPointcut)) {
			return false;
		}
		CflowPointcut o = (CflowPointcut) other;
		return safeSubtreeMatch(node.getBody(), o.getBody());
	}
	public boolean match(AndPointcut node, Object other) {
		if (!(other instanceof AndPointcut)) {
			return false;
		}
		AndPointcut o = (AndPointcut) other;
		return safeSubtreeMatch(node.getLeft(), o.getLeft())
			&& safeSubtreeMatch(node.getRight(), o.getRight());
	}
	public boolean match(OrPointcut node, Object other) {
		if (!(other instanceof OrPointcut)) {
			return false;
		}
		OrPointcut o = (OrPointcut) other;
		return safeSubtreeMatch(node.getLeft(), o.getLeft())
			&& safeSubtreeMatch(node.getRight(), o.getRight());
	}
	public boolean match(BeforeAdviceDeclaration node, Object other) {
		// ajh02: method added
		if (!(other instanceof BeforeAdviceDeclaration)) {
			return false;
		}
		BeforeAdviceDeclaration o = (BeforeAdviceDeclaration) other;
		return  safeSubtreeMatch(node.getJavadoc(), o.getJavadoc())
				&& safeSubtreeListMatch(node.parameters(), o.parameters())
				&& safeSubtreeMatch(node.getPointcut(), o.getPointcut())
				&& safeSubtreeListMatch(node.thrownExceptions(), o.thrownExceptions())
				&& safeSubtreeMatch(node.getBody(), o.getBody());
	}
	
	public boolean match(AfterAdviceDeclaration node, Object other) {
		// ajh02: todo: should have special methods to match
		// afterReturning and afterThrowing
		if (!(other instanceof AfterAdviceDeclaration)) {
			return false;
		}
		AfterAdviceDeclaration o = (AfterAdviceDeclaration) other;
		return  safeSubtreeMatch(node.getJavadoc(), o.getJavadoc())
				&& safeSubtreeListMatch(node.parameters(), o.parameters())
				&& safeSubtreeMatch(node.getPointcut(), o.getPointcut())
				&& safeSubtreeListMatch(node.thrownExceptions(), o.thrownExceptions())
				&& safeSubtreeMatch(node.getBody(), o.getBody());
	}
	
	public boolean match(AroundAdviceDeclaration node, Object other) {
		if (!(other instanceof AroundAdviceDeclaration)) {
			return false;
		}
		AroundAdviceDeclaration o = (AroundAdviceDeclaration) other;
		int level = node.getAST().apiLevel;
		if (level == AST.JLS2_INTERNAL) {
			if (!safeSubtreeMatch(node.internalGetReturnType(), o.internalGetReturnType())) {
				return false;
			}
		}
		if (level >= AST.JLS3) {
			if (!safeSubtreeMatch(node.getReturnType2(), o.getReturnType2())) {
				return false;
			}
			if (!safeSubtreeListMatch(node.typeParameters(), o.typeParameters())) {
				return false;
			}
		}
		return  safeSubtreeMatch(node.getJavadoc(), o.getJavadoc())
				&& safeSubtreeListMatch(node.parameters(), o.parameters())
				&& safeSubtreeMatch(node.getPointcut(), o.getPointcut())
				&& safeSubtreeListMatch(node.thrownExceptions(), o.thrownExceptions())
				&& safeSubtreeMatch(node.getBody(), o.getBody());
	}
	public boolean match(DeclareDeclaration node, Object other) {
		// ajh02: method added
		if (!(other instanceof DeclareDeclaration)) {
			return false;
		}
		DeclareDeclaration o = (DeclareDeclaration) other;
		int level = node.getAST().apiLevel;
		return safeSubtreeMatch(node.getJavadoc(), o.getJavadoc());
	}
	public boolean match(InterTypeFieldDeclaration node, Object other) {
		// ajh02: method added
		if (!(other instanceof InterTypeFieldDeclaration)) {
			return false;
		}
		InterTypeFieldDeclaration o = (InterTypeFieldDeclaration) other;
		int level = node.getAST().apiLevel;
		if (level == AST.JLS2_INTERNAL) {
			if (node.getModifiers() != o.getModifiers()) {
				return false;
			}
		}
		if (level >= AST.JLS3) {
			if (!safeSubtreeListMatch(node.modifiers(), o.modifiers())) {
				return false;
			}
		}
		return 
			safeSubtreeMatch(node.getJavadoc(), o.getJavadoc())
			&& safeSubtreeMatch(node.getType(), o.getType())
			&& safeSubtreeListMatch(node.fragments(), o.fragments());
	}
	public boolean match(InterTypeMethodDeclaration node, Object other) {
		// ajh02: method added
		if (!(other instanceof InterTypeMethodDeclaration)) {
			return false;
		}
		InterTypeMethodDeclaration o = (InterTypeMethodDeclaration) other;
		int level = node.getAST().apiLevel;
		if (level == AST.JLS2_INTERNAL) {
			if (node.getModifiers() != o.getModifiers()) {
				return false;
			}
			if (!safeSubtreeMatch(node.internalGetReturnType(), o.internalGetReturnType())) {
				return false;
			}
		}
		if (level >= AST.JLS3) {
			if (!safeSubtreeListMatch(node.modifiers(), o.modifiers())) {
				return false;
			}
			if (!safeSubtreeMatch(node.getReturnType2(), o.getReturnType2())) {
				return false;
			}
			// n.b. compare type parameters even for constructors
			if (!safeSubtreeListMatch(node.typeParameters(), o.typeParameters())) {
				return false;
			}
		}
		return ((node.isConstructor() == o.isConstructor())
				&& safeSubtreeMatch(node.getJavadoc(), o.getJavadoc())
				&& safeSubtreeMatch(node.getName(), o.getName())
				// n.b. compare return type even for constructors
				&& safeSubtreeListMatch(node.parameters(), o.parameters())
	 			&& node.getExtraDimensions() == o.getExtraDimensions()
				&& safeSubtreeListMatch(node.thrownExceptions(), o.thrownExceptions())
				&& safeSubtreeMatch(node.getBody(), o.getBody()));
	}
	
	public boolean match(DefaultTypePattern node, Object other) {
		return (other instanceof DefaultTypePattern);
	}
	
	public boolean match(SignaturePattern node, Object other) {
		return (other instanceof SignaturePattern);
	}
}
