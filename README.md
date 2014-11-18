resharper-sqale
===============

SonarQube ReSharper SQALE model collaboration

Technical Debt and SQALE remediation costs are moving into a key position in SonarQube. But the SQALE model for ReSharper - one of the two main rule engines for .NET code - has no SQALE model. So ReSharper issues don't currently accrue technical debt.

I'd like to fix that, but I'm not qualified - I'm not a .NET coder, and I'm not familiar with ReSharper rules.

This repo holds a stripped-down version of a SQALE model file, and I'm hoping for help filling it in.

Here's a sample entry. Four spots need data:

      <chc>
        <rule-key>UnassignedField.Local</rule-key>
        <characteristic>      #1a  </characteristic>
        <sub-characteristic>  #1b  </sub-characteristic>
        <prop>
          <key>remediationFactor</key>
          <val>  #2a  </val>
          <txt>  #2b  </txt>
        </prop>
      </chc>

It's easiest to explain them in reverse order

#2 - The remediation time for one issue from this rule
a: numeric time value, E.G. 5
b: textual time unit. One of: min, h, d

What we're looking for is the effort for an average coder to fix the issue on an average day. 
Rule of thumb: 
	trivial effort              = 2 min
	minimal effort              = 5 min
	a little thought required   = 15 min
	thought required            = 30 min
	serious thought required    = 1 h
	major restructuring         = 1 d
  

#1 - How to categorize the technical debt. 
Ask yourself "What's the worst thing that could happen?" and categorize based on the answer. For example, a rule that could be categorized under Maintainability-Understandability or Security-API abuse, should be categorized under Security.

The 1b values are dependant upon the 1a values. For each possible a value, the b values follow:

a: Portability
b: Compiler related portability, Hardware related portability, Language related portability, 
   OS related portability, Software related portability, Time zone related portability

a: Maintainability
b: Readability, Understandability

a: Security
b: API abuse, Errors, Security features, Input validation and representation

a: Efficiency
b: Memory use, Processor use

a:Changeability
b: Architecture related changeability, Data related changeability, Logic related changeability

a: Reliability
b: Architecture related reliability, Data related reliability, Instruction related reliability, 
   Logic related reliability, Synchronization related reliability, Exception handling, Fault tolerance
   Unit tests

a: Testability
b: Unit level testability, Integration  level testability
