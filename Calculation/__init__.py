CONST_R = 0.082
AVOGADRO = 6.02e+23
STP = 22.4


class AtomTheory:
	"""
	Calculator for evey aspects of atom theory
	"""
	
	def __init__(
	self,
	moles=None,
	particles=None,
	mass=None,
	molar=None,
	volume=None,
	temperature=None,
	pressure=None
	):
		self.moles = moles
		self.particles = particles
		self.mass = mass
		self.molar = molar
		self.volume = volume
		self.temp = temperature
		self.press = pressure
		

	def get_particles(self):
		if self.particles is None:
			res = self.moles*AVOGADRO
			return f"Particles: {res} particles"
		elif self.moles is None:
			res = self.particles/AVOGADRO
			return f"Moles: {res}"
	

	def get_mass(self):
		if self.mass is None:
			res = self.moles*self.molar
			return f"Mass: {res} grams"
		elif self.moles is None:
			res = self.mass/self.molar
			return f"Moles: {res} moles"
		elif self.molar is None:
			res = self.mass/self.moles
			return f"Molar Mass: {res} grams/moles"
			

	def get_volume(self, type=None):
			if type == "STP":
					if self.volume is None:
						res = self.moles*STP
						return f"Volume STP: {res} liter"
					elif self.moles is None:
						res = self.volume/STP
						return f"Moles STP: {res} moles"
			
			if self.volume is None:
				res = self.moles*CONST_R*self.temp/self.press
				return f"Volume: {res} liter"
			elif self.moles is None:
				res = (self.volume*self.press)/(CONST_R*self.temp)
				return f"Moles: {res} moles"
			elif self.temp is None:
				res = (self.volume*self.press)/(self.moles*CONST_R)
				return f"Temperature: {res}°K"
			elif self.press is None:
				res = self.moles*CONST_R*self.temp/self.volume
				return f"Pressure: {res} atm"