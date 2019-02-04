from django.db import models

class Classes(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    ClassNumber = models.IntegerField(unique=True)
    Description = models.CharField(max_length=200)

    def __str__(self):
        return "<code: %d, Descr: %s>" %\
                (self.ClassNumber,
                self.Description)


class BalanceAccounts(models.Model): ##??
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    ClassId = models.ForeignKey(Classes, on_delete=models.CASCADE)
    BalanceAccountNumber = models.IntegerField(name='Number', unique=True)

    def __str__(self):
        return "<num: %d>" % (self.Number)

class Files(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    Name = models.CharField(max_length=200)

    def __str__(self):
        return "<Id: %d,Name: %s, DS: %s, DT: %s, Bank: %s>" %\
                (self.Id,
                self.Name)

class Records(models.Model):
    Id = models.IntegerField(primary_key=True, unique=True, auto_created=True)
    FileId = models.ForeignKey(Files, on_delete=models.CASCADE)
    BalanceAccountsId = models.ForeignKey(BalanceAccounts, on_delete=models.CASCADE)

    IncomingBalanceAssets = models.FloatField()
    IncomingBalanceLiabilities = models.FloatField()

    CirculationDebit = models.FloatField()
    CirculationCredit = models.FloatField()

    OutgoingBalanceAssets = models.FloatField()
    OutgoingBalanceLiabilities = models.FloatField()

    def __add__(self,s ):
        self.OutgoingBalanceLiabilities += s.OutgoingBalanceLiabilities
        self.IncomingBalanceAssets += s.IncomingBalanceAssets
        self.IncomingBalanceLiabilities += s.IncomingBalanceLiabilities
        self.OutgoingBalanceAssets += s.OutgoingBalanceAssets
        self.CirculationCredit += s.CirculationCredit
        self.CirculationDebit += s.CirculationDebit
        return self

    def getZerous(self):
        self.IncomingBalanceAssets = 0.0
        self.IncomingBalanceLiabilities = 0.0
        self.CirculationDebit = 0.0
        self.CirculationCredit = 0.0
        self.OutgoingBalanceAssets = 0.0
        self.OutgoingBalanceLiabilities = 0.0
        return self

    def getList(self):
        return [
            self.IncomingBalanceAssets,
            self.IncomingBalanceLiabilities,
            self.CirculationDebit,
            self.CirculationCredit,
            self.OutgoingBalanceAssets,
            self.OutgoingBalanceLiabilities]

    def __str__(self):
        return "<1: %f, 2: %f, 3: %f, 4: %f, 5: %f, 6: %f>" % \
                (
                self.IncomingBalanceAssets,
                self.IncomingBalanceLiabilities,
                self.CirculationDebit,
                self.CirculationCredit,
                self.OutgoingBalanceAssets,
                self.OutgoingBalanceLiabilities)
